import uuid
import random
from datetime import datetime, timedelta
from src.core.db import SessionLocal, engine
from src.models.patient import Patient
from src.models.drug import Drug
from src.models.prescription import Prescription
from src.core.db import Base
from src.utils.logger import logger

def seed_historical_prescriptions():
    logger.info("1 yillik gecmis recete verileri veritabanina ekleniyor...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        patients = db.query(Patient).all()
        drugs = db.query(Drug).all()
        
        if not patients or not drugs:
            logger.warning("Hasta veya ilaç verisi bulunamadı. Lütfen önce hasta ve ilaç verilerini ekleyin.")
            return

        logger.info(f"1 yillik gecmis veri uretimi basliyor. {len(patients)} hasta icin veri uretiliyor...")

        for patient in patients:
            if patient.chronic_disease: 

                annual_visits = random.randint(8, 12)
            elif patient.age < 12 or patient.age > 65: 

                annual_visits = random.randint(4, 7)
            else: 

                annual_visits = random.randint(0, 2)
                
    
            for _ in range(annual_visits):
                days_ago = random.randint(1, 365)
                visit_date = datetime.utcnow() - timedelta(days=days_ago)

                num_drugs = random.randint(1, 3)
                selected_drugs = random.sample(drugs, num_drugs)
                
                for drug in selected_drugs:
                    duration = drug.recommended_duration_days if drug.recommended_duration_days else random.randint(5, 14)
                    
                    presc = Prescription(
                        prescription_id=str(uuid.uuid4()),
                        patient_id=patient.patient_id,
                        drug_id=drug.drug_id,
                        daily_dosage_mg=random.uniform(50.0, 500.0),
                        prescribed_days=duration,
                        created_at=visit_date
                    )
                    logger.info(f"Recete olusturuldu: HastaID={patient.patient_id[:8]} | IlacID={drug.drug_id[:8]} | Tarih={visit_date.strftime('%Y-%m-%d')} | Doz={presc.daily_dosage_mg:.2f}mg | Gun={duration}")
                    db.add(presc)
                    
        db.commit()
        logger.info("1 yillik gecmis recete verileri basariyla veritabanina eklendi.")
        
    except Exception as e:
        logger.error(f"[ERROR] Hata olustu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_historical_prescriptions()