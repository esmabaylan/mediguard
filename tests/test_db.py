import os
import pytest
import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = os.getenv("DB_USER", "mediscope_user")
DB_PASS = os.getenv("DB_PASSWORD", "mediscope_password")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mediscope")

DB_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(DB_URI)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(DB_URI)
    yield engine
    engine.dispose()

def test_db_connection(db_engine):
 
    try:
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Veritabanı bağlantısı kurulamadı: {e}")

def test_create_table_and_insert(db_engine):
    test_df = pd.DataFrame({
        "drug_name": ["TEST_PAROL", "TEST_CALPOL_SURUP"],
        "active_ingredient": ["PARASETAMOL", "PARASETAMOL"],
        "category": ["Ağrı Kesici", "Ağrı Kesici"],
        "is_pediatric": [False, True],
        "is_chronic": [False, False],
        "form": ["Tablet", "Şurup/Süspansiyon/Damla"]
    })
    
    try:
            # Pandas'ın kendi içinde güvenle bağlanması için doğrudan DB_URI string'ini veriyoruz
            test_df.to_sql(
                name="test_drugs_temp",
                con=DB_URI,
                if_exists="replace",
                index=False
            )
    
            # Doğrulama işlemini standart bağlantı ile yap
            with db_engine.connect() as conn:
                count = conn.execute(text("SELECT COUNT(*) FROM test_drugs_temp")).scalar()
                assert count == 2, f"Beklenen 2 satır, ancak {count} satır bulundu."
                
    except Exception as e:
        pytest.fail(f"Tablo oluşturma veya veri ekleme işleminde hata: {e}")
            
    finally:
        with db_engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_drugs_temp"))
            conn.commit()