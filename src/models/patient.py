from sqlalchemy import Column, String, Integer, Float
from src.core.db import Base

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    weight_kg = Column(Float, nullable=True)
    chronic_disease = Column(String, nullable=True)

    @property
    def is_child(self) -> bool:
        return self.age < 18


