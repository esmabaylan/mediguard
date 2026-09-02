from src.core.db import engine, Base

# Sadece 3 ana tablomuzu (Hasta, İlaç, Reçete) import ediyoruz
from src.models.patient import Patient
from src.models.drug import Drug
from src.models.prescription import Prescription

def create_tables():
    print("PostgreSQL'e bağlanılıyor ve tablolar oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    print("Tablolar başarıyla oluşturuldu!")

if __name__ == "__main__":
    create_tables()