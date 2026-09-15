from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.models.drug import Drug
from src.api.schemas.drug import DrugOut

router = APIRouter(prefix="/drugs", tags=["drugs"])


@router.get("", response_model=List[DrugOut])
def list_drugs(
    q: Optional[str] = Query(None, description="İlaç adında arama (opsiyonel)"),
    category: Optional[str] = Query(None, description="Kategoriye göre filtrele (opsiyonel)"),
    db: Session = Depends(get_db),
):
    query = db.query(Drug)

    if q:
        query = query.filter(Drug.name.ilike(f"%{q}%"))
    if category:
        query = query.filter(Drug.category == category)

    return query.order_by(Drug.name).all()