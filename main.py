from fastapi import FastAPI

from impact_routes import router as impact_router

app = FastAPI(
    title="DevDocs Lite - Change Impact Analysis Module",
    description="Standalone module to find affected code parts when code changes."
)

app.include_router(impact_router)


@app.get("/")
def root():
    return {
        "message": "Change Impact Analysis module is running",
        "docs": "/docs",
        "impact_base": "/api/impact"
    }
