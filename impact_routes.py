from change_impact import ChangeImpactService
"""
FastAPI routes for Change Impact Analysis module.

This version is standalone.
Keep this file in the same folder as change_impact.py.
"""

import shutil
import tempfile
import zipfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from change_impact import ChangeImpactService

router = APIRouter(prefix="/api/impact", tags=["Change Impact Analysis"])


def _safe_repo_dir(project_dir: str) -> Path:
    if ".." in Path(project_dir).parts:
        raise HTTPException(status_code=400, detail="Invalid project directory")

    p = Path(project_dir).resolve()

    if not p.is_dir():
        raise HTTPException(status_code=404, detail="Project directory not found")

    return p


class FileImpactRequest(BaseModel):
    project_dir: str
    file_path: str


class SymbolImpactRequest(BaseModel):
    project_dir: str
    file_path: str
    symbol: str


@router.get("/")
def impact_module_info():
    return {
        "module": "Change Impact Analysis",
        "endpoints": [
            "POST /api/impact/file",
            "POST /api/impact/symbol",
            "POST /api/impact/diff"
        ]
    }


@router.post("/file")
def impact_of_file(req: FileImpactRequest):
    """
    If the given file changes, which other files/functions/classes are affected?
    """
    try:
        repo_dir = _safe_repo_dir(req.project_dir)
        service = ChangeImpactService(repo_dir)
        return service.file_impact(req.file_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Impact analysis failed: {e}")


@router.post("/symbol")
def impact_of_symbol(req: SymbolImpactRequest):
    """
    If the given function/class/method changes, which other code parts are affected?
    """
    try:
        repo_dir = _safe_repo_dir(req.project_dir)
        service = ChangeImpactService(repo_dir)
        return service.symbol_impact(req.file_path, req.symbol)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Impact analysis failed: {e}")


@router.post("/diff")
async def impact_of_new_version(
    new_zip: UploadFile = File(...),
    project_dir: str = Form(...),
):
    """
    Compare an existing repository folder with an updated ZIP file.

    This finds:
    - changed files
    - changed functions/classes/methods
    - affected code parts
    - broken references due to deleted symbols
    """
    old_dir = _safe_repo_dir(project_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        extract_dir = Path(temp_dir) / "new_repo"
        extract_dir.mkdir()

        zip_path = extract_dir / (new_zip.filename or "updated_repo.zip")

        with zip_path.open("wb") as f:
            shutil.copyfileobj(new_zip.file, f)

        try:
            with zipfile.ZipFile(zip_path) as zf:
                for member in zf.namelist():
                    dest = (extract_dir / member).resolve()
                    if not str(dest).startswith(str(extract_dir.resolve())):
                        raise HTTPException(
                            status_code=400,
                            detail="Unsafe path inside ZIP file"
                        )

                zf.extractall(extract_dir)
        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid ZIP")

        root = extract_dir
        entries = [e for e in root.iterdir() if e.name != zip_path.name]

        if len(entries) == 1 and entries[0].is_dir():
            root = entries[0]

        try:
            return ChangeImpactService.diff_impact(old_dir, root)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Diff impact analysis failed: {e}")
