from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.models.drug import Drug
from src.models.patient import Patient
from src.models.prescription import Prescription
from src.api.schemas.patient import PatientDetailResponse, PatientInfo, PrescriptionHistoryItem

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/{tckn}", response_model=PatientDetailResponse)
def get_patient(tckn: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == tckn).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")

    rows = (
        db.query(Prescription, Drug)
        .join(Drug, Drug.drug_id == Prescription.drug_id)
        .filter(Prescription.patient_id == tckn)
        .order_by(desc(Prescription.created_at))
        .limit(20)
        .all()
    )

    history = [
        PrescriptionHistoryItem(
            date=presc.created_at,
            drug_id=presc.drug_id,
            drug_name=drug.name,
            dosage_mg=presc.daily_dosage_mg,
            days=presc.prescribed_days,
        )
        for presc, drug in rows
    ]

    return PatientDetailResponse(
        patient_info=PatientInfo.model_validate(patient),
        recent_history=history,
    )