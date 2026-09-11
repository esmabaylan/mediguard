import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from src.core.db import Base

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    risk_type = Column(String)
    severity = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)