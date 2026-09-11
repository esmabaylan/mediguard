from src.risk_engine.base_risk import BaseRiskRule
from typing import List, Dict

class PainkillerRisk(BaseRiskRule):
    def evaluate(self, event: dict) -> List[Dict]:
        alerts = []
        medications = event.get("medications", [])
        
        painkillers = [med for med in medications if med.get("drug_category") == "Ağrı Kesici"]
        
        if len(painkillers) > 1:
            drug_names = ", ".join([p.get("drug_name") for p in painkillers])
            alerts.append({
                "risk_type": "PAINKILLER_DUPLICATION",
                "severity": "WARNING",
                "prescription_id": event.get("prescription_id"),
                "patient_id": event.get("patient_id"),
                "message": f"Coklu Agri Kesici Kullanimi: Ayni recetede birden fazla agri kesici ({drug_names}) tespit edildi. Toksisite riski."
            })
        
        return alerts