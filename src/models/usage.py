from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from src.core.db import Base

class MedicationUsage(Base):
    __tablename__ = "medication_usage"
    
    usage_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    drug_id = Column(String, ForeignKey("drugs.drug_id"), nullable=False)
    usage_start_date = Column(Date, nullable=False)
    usage_end_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    daily_dose = Column(Float, nullable=False)
    usage_days = Column(Integer, nullable=False)