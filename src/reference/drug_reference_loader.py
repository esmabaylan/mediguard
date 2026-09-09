import uuid
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import uuid
import sys
import os
from sqlalchemy import create_engine
from src.core.db import Base
from src.models.drug import Drug 
from src.core.config import settings


CSV_PATH = r"/app/data/raw/processed/titck_enriched_clean.csv"

def load_csv():
    print("CSV okunuyor...")
    df = pd.read_csv(CSV_PATH)
    print(f"  {len(df)} satır, {len(df.columns)} kolon okundu.")
    return df


def transform_data(df):
    print("Veri ORM şemasına uygun olarak dönüştürülüyor...")
    
    df['drug_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    

    df['name'] = df['drug_name']

    df['strength'] = None
    df['strength_unit'] = None
    df['box_quantity'] = 1
    
    df['usage_type'] = df['is_chronic'].apply(lambda x: "TIP2_KRONIK" if x else "TIP1_GECICI")

    df['is_weight_based'] = df['is_pediatric'].astype(bool)
    
    df['max_daily_dose'] = None
    df['max_daily_dose_unit'] = None
    df['weight_based_dose_mg_kg'] = None
    df['recommended_duration_days'] = None
    

    db_cols = [
        "drug_id", "name", "category", "active_ingredient", "form",
        "strength", "strength_unit", "box_quantity", "usage_type",
        "is_weight_based", "max_daily_dose", "max_daily_dose_unit",
        "weight_based_dose_mg_kg", "recommended_duration_days"
    ]
    
    return df[db_cols]
def insert_data(df):
    print("Veritabanına bağlanılıyor ve veriler aktarılıyor...")
    conn = psycopg2.connect(settings.DB_URI)
    cur = conn.cursor()

    db_cols = [
        "drug_id", "name", "category", "active_ingredient", "form",
        "strength", "strength_unit", "box_quantity", "usage_type",
        "is_weight_based", "max_daily_dose", "max_daily_dose_unit",
        "weight_based_dose_mg_kg", "recommended_duration_days"
    ]

    df_insert = df[db_cols]
    
    placeholders = ", ".join(["%s"] * len(db_cols))
    col_names = ", ".join(db_cols)

    insert_sql = f"""
        INSERT INTO drugs ({col_names})
        VALUES ({placeholders})
        ON CONFLICT (drug_id) DO NOTHING
    """

  
    rows = [tuple(x) for x in df_insert.to_numpy()]

    print(f"  {len(rows)} satır yükleniyor (batch=1000)...")
    execute_batch(cur, insert_sql, rows, page_size=1000)
    conn.commit()

    cur.close()
    conn.close()
    print("  Aktarım tamamlandı.")

def verify():
    print("Veriler doğrulanıyor...")
    conn = psycopg2.connect(settings.DB_URI)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM drugs;")
    count = cur.fetchone()[0]
    print(f"  drugs tablosundaki toplam satır: {count}")

    cur.execute("""
        SELECT category, COUNT(*)
        FROM drugs
        GROUP BY category
        ORDER BY COUNT(*) DESC;
    """)
    print("  Kategori Dağılımı:")
    for row in cur.fetchall():
        print(f"    {row[0]}: {row[1]} ilaç")

    cur.close()
    conn.close()

if __name__ == "__main__":
    try:


        print("Veritabanı şeması kontrol ediliyor...")
     
        engine_uri = settings.DB_URI
        engine = create_engine(engine_uri)
        Base.metadata.create_all(bind=engine)
        print("Tablo şeması hazır!")

    
        raw_df = load_csv()
        transformed_df = transform_data(raw_df)
        insert_data(transformed_df)
        verify()
        print("\nİşlem Başarılı!")
    except Exception as e:
        print(f"\nHata: {e}")
        sys.exit(1)