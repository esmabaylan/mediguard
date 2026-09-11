from src.risk_engine.pediatric_risk import PediatricRisk
from src.risk_engine.painkiller_risk import PainkillerRisk
from src.risk_engine.stomach_risk import StomachRisk

class RiskDispatcher:
    def __init__(self):
        self.active_rules = [
            PediatricRisk(),
            PainkillerRisk(),
            StomachRisk()
        ]

    def analyze(self, event: dict) -> list:
        all_alerts = []
        for rule in self.active_rules:
            alerts = rule.evaluate(event)
            if alerts:
                all_alerts.extend(alerts)
        return all_alerts