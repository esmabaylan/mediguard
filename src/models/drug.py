from sqlalchemy import Column, String, Integer, Float, Boolean
from src.core.db import Base


class Drug(Base):
    __tablename__ = "drugs"

    # Identity
    drug_id = Column(String, primary_key=True, index=True)

    # Basic Information
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    active_ingredient = Column(String, nullable=False)

    # Pharmaceutical Information
    form = Column(String, nullable=False)
    strength = Column(Float, nullable=True)
    strength_unit = Column(String, nullable=True)

    box_quantity = Column(Integer, nullable=False)

    # Usage Information
    usage_type = Column(String, nullable=False)
    is_weight_based = Column(Boolean, default=False)

    # Risk Reference Information
    max_daily_dose = Column(Float, nullable=True)
    max_daily_dose_unit = Column(String, nullable=True)

    weight_based_dose_mg_kg = Column(Float, nullable=True)

    recommended_duration_days = Column(Integer, nullable=True)