import os
import random
import uuid
import pandas as pd
from sqlalchemy import create_engine
import sys
from src.core.config import settings
from src.utils.logger import logger

from src.core.db import Base
from src.models.patient import Patient
from src.utils.helpers import generate_mock_person, generate_mock_tckn


def generate_patients(num_patients=10000):
    logger.info(f"{num_patients} adet sentetik hasta üretiliyor...")
    patients = []
    
    chronic_diseases_list = ["Hipertansiyon", "Tip 2 Diyabet", "Astım", "KOAH", "Kalp Yetmezliği", None, None, None]
    
    for _ in range(num_patients):
        age = random.randint(1, 85)
        

        if age == 1:
            weight_kg = round(random.uniform(7.0, 11.5), 1)   # 1 yaş bebek
        elif age == 2:
            weight_kg = round(random.uniform(10.0, 14.5), 1)  # 2 yaş
        elif age <= 5:
            weight_kg = round(random.uniform(14.0, 21.0), 1)  # 3-5 yaş okul öncesi
        elif age <= 8:
            weight_kg = round(random.uniform(20.0, 30.0), 1)  # 6-8 yaş
        elif age <= 12:
            weight_kg = round(random.uniform(30.0, 45.0), 1)  # 9-12 yaş
        elif age <= 16:
            weight_kg = round(random.uniform(45.0, 65.0), 1)  # 13-16 yaş ergenlik
        else:
            weight_kg = round(random.uniform(50.0, 110.0), 1) # Yetişkin
            
        if age < 18:

            if random.random() < 0.14:
                chronic = random.choice(["Astım", "Tip 1 Diyabet", "Epilepsi", "Kistik Fibrozis"])
            else:
                chronic = None
        else:
            
    

            chronic = random.choice(["Hipertansiyon", "Tip 2 Diyabet", "Astım", "KOAH", "Kalp Yetmezliği", None, None, None])
        cinsiyet, ad, soyad = generate_mock_person()
        patients.append({
            "patient_id": generate_mock_tckn(),
            "first_name": ad,
            "last_name": soyad,
            "gender": cinsiyet,
            "age": age,
            "weight_kg": weight_kg,
            "chronic_disease": chronic
        })
        
    return pd.DataFrame(patients)

if __name__ == "__main__":
    try:
        logger.info("Veritabanı şeması kontrol ediliyor...")
        engine_uri = settings.DB_URI
        engine = create_engine(engine_uri)
        
        Base.metadata.create_all(bind=engine)
        
        df_patients = generate_patients(10000)
        
        with engine.begin() as conn:
            df_patients.to_sql("patients", con=conn, if_exists="append", index=False)
            
        logger.info(f"\nİşlem Başarılı: {len(df_patients)} hasta veritabanına eklendi.")
    except Exception as e:
        logger.error(f"\nHata: {e}")
        sys.exit(1)