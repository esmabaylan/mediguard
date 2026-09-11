from src.core.db import engine, Base

# Sadece 3 ana tablomuzu (Hasta, İlaç, Reçete) import ediyoruz
from src.models.patient import Patient
from src.models.drug import Drug
from src.models.prescription import Prescription
from src.utils.logger import logger

def create_tables():
    logger.info("Veritabanı tabloları oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    logger.info("Veritabanı tabloları başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_tables()