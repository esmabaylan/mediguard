from sqlalchemy import Column, String, Integer, Double, DateTime, ForeignKey
from src.core.db import Base
from datetime import datetime

class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    drug_id = Column(String, ForeignKey("drugs.drug_id"))
    daily_dosage_mg = Column(Double)
    prescribed_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)