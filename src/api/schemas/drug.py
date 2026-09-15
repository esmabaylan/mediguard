from typing import Optional

from pydantic import BaseModel, ConfigDict


class DrugOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    drug_id: str
    name: str
    category: str
    active_ingredient: str
    form: str
    strength: Optional[float] = None
    strength_unit: Optional[str] = None
    max_daily_dose: Optional[float] = None
    max_daily_dose_unit: Optional[str] = None
    recommended_duration_days: Optional[int] = None