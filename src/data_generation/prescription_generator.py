import os
import time
import uuid
import random
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.db import Base
from src.models.prescription import Prescription
from src.models.alert import Alert 

DB_URI = f"postgresql://{os.getenv('DB_USER', 'mediscope_user')}:{os.getenv('DB_PASSWORD', 'mediscope_password')}@{os.getenv('DB_HOST', 'postgres')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'mediscope')}"

INTERACTION_RULES = {
    "Kolesterol": ["Antibiyotik", "Antiviral"],
    "Kalp/Tansiyon": ["Ağrı Kesici"],
    "Psikiyatri": ["Sinir Sistemi-Bağımlılık Riskli", "Ağrı Kesici"],
    "Mide": ["Antibiyotik"]
}

def get_reference_data(engine):
    patients_df = pd.read_sql("SELECT patient_id, age, weight_kg, chronic_disease FROM patients", engine)
    drugs_df = pd.read_sql("SELECT drug_id, category, is_weight_based FROM drugs", engine)
    return patients_df, drugs_df

def check_drug_interaction(session, patient_id, new_category, drugs_df):
    past_prescriptions = session.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    if not past_prescriptions:
        return False, None
        
    past_drug_ids = [rx.drug_id for rx in past_prescriptions]
    past_categories = drugs_df[drugs_df['drug_id'].isin(past_drug_ids)]['category'].tolist()
    
    for past_cat in past_categories:
        if past_cat in INTERACTION_RULES.get(new_category, []) or new_category in INTERACTION_RULES.get(past_cat, []):
            return True, past_cat
            
    return False, None

def generate_and_save_prescription(session, patients_df, drugs_df):
    patient = patients_df.sample(1).iloc[0]
    drug = drugs_df.sample(1).iloc[0]
    
    is_conflict, conflicting_category = check_drug_interaction(session, patient['patient_id'], drug['category'], drugs_df)
    
    if is_conflict:

        new_alert = Alert(
            alert_id=str(uuid.uuid4()),
            patient_id=patient['patient_id'],
            alert_type="DDI_BLOCKED",
            attempted_category=drug['category'],
            conflicting_category=conflicting_category,
            created_at=datetime.utcnow()
        )
        session.add(new_alert)
        session.commit()
        
        print(f"[BLOKE & LOGLANDI] Hasta: {patient['patient_id'][:8]} | Yeni: {drug['category']} <-> Eski: {conflicting_category}!")
        return None
    
    base_dose = random.uniform(50.0, 500.0)
    if patient['age'] < 18 and drug['is_weight_based']:
        daily_dose = round(base_dose * (patient['weight_kg'] / 10), 1) 
    else:
        daily_dose = round(base_dose, 1)

    new_prescription = Prescription(
        prescription_id=str(uuid.uuid4()),
        patient_id=patient['patient_id'],
        drug_id=drug['drug_id'],
        daily_dosage_mg=daily_dose,
        frequency_per_day=random.randint(1, 4),
        duration_days=random.randint(3, 30),
        created_at=datetime.utcnow()
    )
    
    session.add(new_prescription)
    session.commit()
    
    print(f"[KAYDEDİLDİ] Hasta: {patient['patient_id'][:8]} | İlaç: {drug['category']} | Doz: {daily_dose}mg")
    return new_prescription

def start_prescription_stream():
    engine = create_engine(DB_URI)
    Base.metadata.create_all(bind=engine) 
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    patients_df, drugs_df = get_reference_data(engine)
    
    print("Loglamalı Risk Motoru başlatıldı! (Çıkış için CTRL+C)")
    session = SessionLocal()
    try:
        while True:
            generate_and_save_prescription(session, patients_df, drugs_df)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAkış durduruldu.")
    finally:
        session.close()

if __name__ == "__main__":
    start_prescription_stream()