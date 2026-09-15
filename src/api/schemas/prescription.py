from typing import List, Optional

from pydantic import BaseModel


class MedicationItem(BaseModel):
    drug_id: str
    drug_category: str
    daily_dosage_mg: float
    prescribed_days: int


class PrescriptionAnalyzeRequest(BaseModel):
    patient_id: str
    medications: List[MedicationItem]


class AlertOut(BaseModel):
    risk_type: str
    severity: Optional[str] = "warning"
    message: str


class PrescriptionAnalyzeResponse(BaseModel):
    status: str  # "OK" | "RISK_FOUND"
    alerts: List[AlertOut] = []


class PrescriptionSaveResponse(BaseModel):
    prescription_id: str
    status: str