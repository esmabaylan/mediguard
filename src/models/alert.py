from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from src.core.db import Base

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    
    alert_type = Column(String, nullable=False)
    attempted_category = Column(String, nullable=False)
    conflicting_category = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)