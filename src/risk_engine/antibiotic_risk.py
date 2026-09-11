import datetime
from typing import List, Dict

from src.risk_engine.base_risk import BaseRiskRule
from src.core.db import SessionLocal
from src.models.drug import Drug
from src.models.prescription import Prescription
from src.utils.logger import logger

class AntibioticRisk(BaseRiskRule):
    def evaluate(self, event: dict) -> List[Dict]:
        alerts = []
        medications = event.get("medications", [])
        patient_id = event.get("patient_id")
        
        antibiotics = [med for med in medications if med.get("drug_category") == "Antibiyotik"]
        if not antibiotics:
            return alerts

        db = SessionLocal()
        try:
            for med in antibiotics:
               
                actual_drug = db.query(Drug).filter(Drug.drug_id == med.get("drug_id")).first()
                if not actual_drug:
                    continue
                    
                active_ingredient = actual_drug.active_ingredient
                
                
                one_year_ago = datetime.datetime.utcnow() - datetime.timedelta(days=365)
                past_annual_usage = db.query(Prescription).join(Drug).filter(
                    Prescription.patient_id == patient_id,
                    Drug.active_ingredient == active_ingredient,
                    Prescription.created_at >= one_year_ago
                ).count()
                
                
                if past_annual_usage >= 3:
                    alerts.append({
                        "risk_type": "ANTIBIOTIC_ANNUAL_RESISTANCE",
                        "severity": "WARNING",
                        "prescription_id": event.get("prescription_id"),
                        "patient_id": patient_id,
                        "drug_id": med.get("drug_id"),
                        "message": f"AMR Riski: Hasta son 1 yilda {past_annual_usage} kez '{active_ingredient}' etken maddesini kullanmis."
                    })
        except Exception as e:
            logger.error(f"[WARNING] AntibioticRisk kuralinda hata: {e}")
        finally:
            db.close()
            
        return alerts