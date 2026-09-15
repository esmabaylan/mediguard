from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PatientInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str
    first_name: str
    last_name: str
    age: int
    gender: str
    chronic_disease: Optional[str] = None


class PrescriptionHistoryItem(BaseModel):
    date: datetime
    drug_id: str
    drug_name: Optional[str] = None
    dosage_mg: float
    days: int


class PatientDetailResponse(BaseModel):
    patient_info: PatientInfo
    recent_history: List[PrescriptionHistoryItem]