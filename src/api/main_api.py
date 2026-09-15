from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import drugs, patients, prescriptions

app = FastAPI(title="MediGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/api")
app.include_router(prescriptions.router, prefix="/api")
app.include_router(drugs.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}