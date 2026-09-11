from src.risk_engine.base_risk import BaseRiskRule
from typing import List, Dict

class StomachRisk(BaseRiskRule):
    def evaluate(self, event: dict) -> List[Dict]:
        alerts = []
        age = event.get("patient_age", 0)
        medications = event.get("medications", [])
        
        
        categories = [med.get("drug_category", "General") for med in medications]
        
        
        if age >= 60 and "Ağrı Kesici" in categories and "Mide Koruyucu" not in categories:
            alerts.append({
                "risk_type": "MISSING_STOMACH_PROTECTOR",
                "severity": "WARNING",
                "prescription_id": event.get("prescription_id"),
                "patient_id": event.get("patient_id"),
                "message": f"Mide Koruyucu Eksik: 60 yas ustu ({age}) hastaya Agri Kesici yazilmis ancak Mide Koruyucu eklenmemis. Ulser/Kanama riski!"
            })
            
        return alerts