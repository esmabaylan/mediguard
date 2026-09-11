import json
import time

from kafka import KafkaConsumer, KafkaProducer
from src.core.config import settings
from src.risk_engine.risk_dispatcher import RiskDispatcher
from src.utils.logger import logger

def start_prescription_consumer():
    logger.info("[INFO] Risk Analiz Motoru (Consumer & Alert Producer) Baslatiliyor...")
    try:
        
        alert_producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        
        consumer = KafkaConsumer(
            settings.PRESCRIPTION_TOPIC,
            bootstrap_servers=settings.KAFKA_BROKER,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='mediguard_risk_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        logger.info(f"[INFO] Tuketici Baglandi. Dinlenen Topic: {settings.PRESCRIPTION_TOPIC}")
        
        risk_engine = RiskDispatcher()
        
        for message in consumer:
            event = message.value
            prescription_id = event.get('prescription_id', 'Bilinmiyor')
            patient_id = event.get('patient_id', 'Bilinmiyor')
            medications = event.get('medications', [])
            
            drug_names = [med.get('drug_name', 'Bilinmiyor') for med in medications]
            drugs_str = ", ".join(drug_names)
            
            logger.info(f"[STREAM] Yakalandi | ID: {str(prescription_id)[:8]} | Hasta: {str(patient_id)[:8]} | Ilac Sayisi: {len(medications)} -> [{drugs_str}]")
            
            
            alerts = risk_engine.analyze(event)
            
            if alerts:
                for alert in alerts:
                    logger.info(f"   [ALARM] {alert['severity']} | {alert['risk_type']} | {alert['message']}")
                    
                    alert['alert_timestamp'] = time.time()
                    alert_producer.send(settings.ALERTS_TOPIC, alert)
                    
    except KeyboardInterrupt:
        logger.info("\n[INFO] Tuketici servisi durduruldu.")
    except Exception as e:
        logger.error(f"[ERROR] Tuketici/Motor Hatasi: {str(e)}")
    finally:
        if 'consumer' in locals():
            consumer.close()
        if 'alert_producer' in locals():
            alert_producer.close()

if __name__ == "__main__":
    start_prescription_consumer()