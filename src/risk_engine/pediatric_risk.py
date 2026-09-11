from src.risk_engine.base_risk import BaseRiskRule
from typing import List, Dict

class PediatricRisk(BaseRiskRule):
    def evaluate(self, event: dict) -> List[Dict]:
        alerts = []
        age = event.get("patient_age")
        weight = event.get("patient_weight")
        medications = event.get("medications", [])

        
        if age is not None and age < 18 and weight:
            for med in medications:
                dose = med.get("daily_dosage_mg", 0)
                
                
                max_safe_dose = weight * 15.0
                
                if dose > max_safe_dose:
                    alerts.append({
                        "risk_type": "PEDIATRIC_OVERDOSE",
                        "severity": "CRITICAL",
                        "prescription_id": event.get("prescription_id"),
                        "patient_id": event.get("patient_id"),
                        "drug_id": med.get("drug_id"),
                        "message": f"Kritik Doz Asimi: {med.get('drug_name')} icin {dose}mg recete edildi. Hastanin kilosuna ({weight}kg) gore maksimum guvenli doz {max_safe_dose:.1f}mg olmalidir."
                    })
        
        return alerts