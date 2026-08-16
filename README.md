# DevDocs Lite - Change Impact Analysis Module

## Module Objective

When any code changes in an existing project/codebase, this module automatically identifies which other code parts are affected by that change.

In simple words:

> If a file, function, class, or method changes, this module finds the dependent files, functions, classes, and methods.

## Features

- File-level impact analysis
- Symbol-level impact analysis
- Function/class/method dependency detection
- Import dependency detection
- Inheritance dependency detection
- Old repository vs updated repository diff impact analysis
- Detects changed, added, and removed symbols
- Detects possible broken references when symbols are removed

## Files

| File | Purpose |
|---|---|
| `change_impact.py` | Core impact analysis engine |
| `impact_routes.py` | FastAPI endpoints |
| `main.py` | Standalone FastAPI application |
| `test_module.py` | Simple local test |
| `requirements.txt` | Required Python packages |

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the module:

```bash
uvicorn main:app --reload
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. File Impact

```text
POST /api/impact/file
```

Example request body:

```json
{
  "project_dir": "C:/full/path/to/target_repo",
  "file_path": "utils.py"
}
```

### 2. Symbol Impact

```text
POST /api/impact/symbol
```

Example request body:

```json
{
  "project_dir": "C:/full/path/to/target_repo",
  "file_path": "utils.py",
  "symbol": "calculate_tax"
}
```

### 3. Diff Impact

```text
POST /api/impact/diff
```

This accepts:

- `project_dir`: existing repository path
- `new_zip`: updated repository ZIP file

## Simple Test

Run:

```bash
python test_module.py
```

This creates a small sample repository and shows affected code parts automatically.

## Integration with DevDocs Lite

This module can be integrated into the main DevDocs Lite project by placing:

- `change_impact.py` inside `app/services/`
- `impact_routes.py` inside `app/api/`

Then register the router in the main FastAPI app:

```python
from app.api.impact_routes import router as impact_router

app.include_router(impact_router)
```

## Module Role in DevDocs Lite

This module adds a deterministic code-change impact analysis layer to DevDocs Lite. It uses Python AST analysis to build a dependency graph and answers questions such as:

- If this file changes, which files are affected?
- If this function changes, which functions call it?
- If this class changes, which classes inherit or use it?
- If this symbol is removed, which references may break?
