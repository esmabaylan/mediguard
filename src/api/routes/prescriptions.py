import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.models.prescription import Prescription
from src.api.schemas.prescription import (
    PrescriptionAnalyzeRequest,
    PrescriptionAnalyzeResponse,
    PrescriptionSaveResponse,
)
from src.services.risk_service import run_risk_analysis

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.post("/analyze", response_model=PrescriptionAnalyzeResponse)
def analyze_prescription(payload: PrescriptionAnalyzeRequest, db: Session = Depends(get_db)):
    alerts = run_risk_analysis(payload, db)
    status = "RISK_FOUND" if alerts else "OK"
    return PrescriptionAnalyzeResponse(status=status, alerts=alerts)


@router.post("/save", response_model=PrescriptionSaveResponse)
def save_prescription(payload: PrescriptionAnalyzeRequest, db: Session = Depends(get_db)):
    prescription_id = str(uuid.uuid4())

    for med in payload.medications:
        db.add(
            Prescription(
                prescription_id=prescription_id,
                drug_id=med.drug_id,
                patient_id=payload.patient_id,
                daily_dosage_mg=med.daily_dosage_mg,
                prescribed_days=med.prescribed_days,
            )
        )

    db.commit()

    return PrescriptionSaveResponse(prescription_id=prescription_id, status="SAVED")