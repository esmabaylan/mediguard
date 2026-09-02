from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from src.core.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    prescription_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    drug_id = Column(String, ForeignKey("drugs.drug_id"), nullable=False)
    prescribed_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    daily_dose = Column(Float, nullable=False)
    planned_usage_days = Column(Integer, nullable=False)