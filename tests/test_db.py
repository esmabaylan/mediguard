import os
import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from src.core.config import settings

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(settings.DB_URI)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(settings.DB_URI)
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

            test_df.to_sql(
                name="test_drugs_temp",
                con=settings.DB_URI,
                if_exists="replace",
                index=False
            )
    

            with db_engine.connect() as conn:
                count = conn.execute(text("SELECT COUNT(*) FROM test_drugs_temp")).scalar()
                assert count == 2, f"Beklenen 2 satır, ancak {count} satır bulundu."
                
    except Exception as e:
        pytest.fail(f"Tablo oluşturma veya veri ekleme işleminde hata: {e}")
            
    finally:
        with db_engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_drugs_temp"))
            conn.commit()