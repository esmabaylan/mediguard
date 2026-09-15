from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from src.core.db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(String, primary_key=True, index=True)
    
    # Not: Eğer "drugs" tablon henüz rastgele ilaçlarla dolu değilse, DB_WRITER'ın
    # ForeignKey hatasıyla çökmemesi için burayı şimdilik düz String bırakmak daha güvenlidir.
    drug_id = Column(String, primary_key=True) 
    
    # API'deki 500 hatasını çözecek ve tabloları bağlayacak kritik referans:
    patient_id = Column(String, ForeignKey("patients.patient_id"), index=True)
    
    daily_dosage_mg = Column(Float)
    prescribed_days = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)