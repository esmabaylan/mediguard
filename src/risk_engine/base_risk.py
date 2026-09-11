from abc import ABC, abstractmethod
from typing import List, Dict

class BaseRiskRule(ABC):
    """Tüm risk değerlendirme sınıflarının uyması gereken temel şablon."""
    
    @abstractmethod
    def evaluate(self, event: dict) -> List[Dict]:
        """
        Gelen Kafka event'ini analiz eder.
        Risk bulunmazsa boş liste [], bulunursa uyarı (alert) sözlüklerinden oluşan bir liste döner.
        """
        pass