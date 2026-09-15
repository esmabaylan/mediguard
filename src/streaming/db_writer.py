import json
from kafka import KafkaConsumer

from src.core.config import settings
from src.core.db import SessionLocal, engine, Base
from src.models.prescription import Prescription
from src.models.alert import Alert
from src.utils.logger import logger
from src.models.patient import Patient
# from src.models.drug import Drug

def start_db_writer():
    logger.info("[INFO] Veritabani Yazici (DB Writer) Servisi Baslatiliyor...")
    Base.metadata.create_all(bind=engine) 
    
    consumer = KafkaConsumer(
        bootstrap_servers=settings.KAFKA_BROKER,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='mediguard_db_writer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    consumer.subscribe([settings.PRESCRIPTION_TOPIC, settings.ALERTS_TOPIC])
    logger.info(f"[INFO] Dinlenen Kanallar: {settings.PRESCRIPTION_TOPIC} & {settings.ALERTS_TOPIC}")
    
    db = SessionLocal()
    
    # DİKKAT: Sonsuz döngü en dışta, try-except içeride!
    for message in consumer:
        try:
            event = message.value
            topic = message.topic
            
            if topic == settings.PRESCRIPTION_TOPIC:
                prescription_id = event.get("prescription_id")
                patient_id = event.get("patient_id")
                
                for med in event.get("medications", []):
                    presc_record = Prescription(
                        prescription_id=prescription_id,
                        patient_id=patient_id,
                        drug_id=med.get("drug_id"),
                        daily_dosage_mg=med.get("daily_dosage_mg"),
                        prescribed_days=med.get("prescribed_days", 7) 
                    )
                    db.add(presc_record)
                
                db.commit()
                logger.info(f"[DB KAYIT] Recete islendi: {prescription_id[:8]}")
                
            elif topic == settings.ALERTS_TOPIC:
                alert_record = Alert(
                    prescription_id=event.get("prescription_id"),
                    patient_id=event.get("patient_id"),
                    risk_type=event.get("risk_type"),
                    severity=event.get("severity"),
                    message=event.get("message")
                )
                db.add(alert_record)
                db.commit()
                logger.info(f"[DB KAYIT] ALARM islendi: {event.get('risk_type')}")
                
        except Exception as e:
            # Hata alırsak sadece o anki işlemi geri al, döngüyü bozma!
            db.rollback()
            logger.warning(f"[ATLANDI] Gecersiz veri (Muhtemelen kayitsiz TCKN). Hata: {str(e)[:50]}...")

if __name__ == "__main__":
    start_db_writer()