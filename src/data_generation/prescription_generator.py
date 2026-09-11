import json
import time
import random
import uuid
from kafka import KafkaProducer
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.db import SessionLocal
from src.models.patient import Patient
from src.models.drug import Drug
from src.utils.logger import logger

def start_generating_prescriptions():
    logger.info("[INFO] Recete Uretici (Producer) baslatiliyor...")
    
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        retries=3
    )
    
    db: Session = SessionLocal()
    
    try:
        patients = db.query(Patient).all()
        drugs = db.query(Drug).all()
        
        if not patients or not drugs:
            logger.error("[ERROR] Veritabaninda hasta veya ilac bulunamadi.")
            return

        logger.info("[INFO] Simulasyon basladi. Coklu ilac icerebilen receteler uretiliyor...")
        
        while True:
            patient = random.choice(patients)
            
            # 1 ile 4 arası rastgele sayıda ilaç seç (Aynı ilacı tekrar seçmemek için sample kullanıyoruz)
            num_drugs = random.randint(1, 4)
            selected_drugs = random.sample(drugs, num_drugs)
            
            # Seçilen ilaçları bir listeye doldur
            medications = []
            for drug in selected_drugs:
                medications.append({
                    "drug_id": str(drug.drug_id),
                    "drug_name": drug.name,
                    "drug_category": getattr(drug, 'category', 'General'),
                    "daily_dosage_mg": random.randint(10, 500)
                })
            
            # Yeni JSON şablonumuz (Artık tek bir drug_id yerine medications listesi var)
            event = {
                "prescription_id": str(uuid.uuid4()),
                "patient_id": str(patient.patient_id),
                "patient_age": patient.age,
                "patient_weight": float(patient.weight_kg) if patient.weight_kg else None,
                "medications": medications,
                "timestamp": time.time()
            }
            
            producer.send(settings.PRESCRIPTION_TOPIC, event)
            time.sleep(random.uniform(0.5, 2.0))
            
    except Exception as e:
        logger.error(f"[ERROR] Uretici motorunda hata: {str(e)}")
    finally:
        db.close()
        producer.close()