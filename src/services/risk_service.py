from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from src.models.drug import Drug
from src.models.patient import Patient
from src.risk_engine.risk_dispatcher import RiskDispatcher
from src.api.schemas.prescription import PrescriptionAnalyzeRequest

# Dispatcher tek seferlik oluşturulur (kural listesi sabit, her istek için
# yeniden instantiate etmeye gerek yok).
_dispatcher = RiskDispatcher()


def _build_event(
    payload: PrescriptionAnalyzeRequest,
    db: Session,
    prescription_id: Optional[str] = None,
) -> Dict:
    """Frontend'den gelen isteği, risk_engine kurallarının beklediği event
    formatına çevirir. Kategori ve ilaç adı gibi kritik alanlar DB'den
    (Drug tablosundan) alınır - frontend'in gönderdiği değere güvenilmez,
    böylece 'Ağrı Kesici' / 'Antibiyotik' gibi string eşleşmeleri her zaman
    veritabanındaki tek doğru kaynakla tutarlı kalır."""

    patient = db.query(Patient).filter(Patient.patient_id == payload.patient_id).first()

    enriched_meds = []
    for med in payload.medications:
        drug = db.query(Drug).filter(Drug.drug_id == med.drug_id).first()
        enriched_meds.append({
            "drug_id": med.drug_id,
            "drug_name": drug.name if drug else med.drug_id,
            "drug_category": drug.category if drug else med.drug_category,
            "daily_dosage_mg": med.daily_dosage_mg,
            "prescribed_days": med.prescribed_days,
        })

    return {
        "prescription_id": prescription_id,
        "patient_id": payload.patient_id,
        "patient_age": patient.age if patient else None,
        "patient_weight": patient.weight_kg if patient else None,
        "medications": enriched_meds,
    }


def run_risk_analysis(
    payload: PrescriptionAnalyzeRequest,
    db: Session,
    prescription_id: Optional[str] = None,
) -> List[Dict]:
    """API katmanının çağıracağı tek fonksiyon. Event'i kurar, dispatcher'ı
    çalıştırır ve alert listesini döner (boşsa risk yok demektir)."""
    event = _build_event(payload, db, prescription_id)
    return _dispatcher.analyze(event)