import os
import argparse
import logging

from src.reference.titck_scraper import parse_titck_table
from src.reference.drug_reference_loader import process_and_save
# from src.database.load_csv_to_postgres import load_drugs_to_postgres

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_data_pipeline(force_scrape=False, force_enrich=False):
    raw_csv = "data/raw/drug_reference/titck_drugs_extracted.csv"
    enriched_csv = "C:\\Users\\esman\\Documents\\Github\\mediguard\\data\\raw\\processed\\titck_enriched_clean.csv"


    # if os.path.exists(raw_csv) and not force_scrape:
    #     logging.info("1. TİTCK ham verisi zaten mevcut. Scraping adımı atlanıyor. (Zorlamak için --force-scrape kullanın)")
    # else:
    #     logging.info("1. TİTCK verileri çekiliyor...")
    #     # Eğer eski dosya varsa ve force edildiyse, üzerine yazmadan önce eskiyi silmek iyi bir pratiktir
    #     if os.path.exists(raw_csv): os.remove(raw_csv)
    #     parse_titck_table()


    # if os.path.exists(enriched_csv) and not force_enrich:
    #     logging.info("2. Zenginleştirilmiş veri zaten mevcut. Sınıflandırma adımı atlanıyor.")
    # else:
    #     logging.info("2. Veriler zenginleştiriliyor ve sınıflandırılıyor...")
    #     process_and_save(input_file=raw_csv, output_file=enriched_csv)


    logging.info("3. Veriler PostgreSQL veritabanına aktarılıyor...")
    load_drugs_to_postgres(csv_path=enriched_csv)
    
    logging.info("Boru hattı (Pipeline) işlemi tamamlandı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediGuard Data Pipeline Orkestratörü")
    parser.add_argument("--force-scrape", action="store_true", help="Var olan ham veriyi ezer ve TİTCK sitesinden baştan çeker.")
    parser.add_argument("--force-enrich", action="store_true", help="Var olan temizlenmiş veriyi ezer ve yeniden sınıflandırır.")
    
    args = parser.parse_args()
    run_data_pipeline(force_scrape=args.force_scrape, force_enrich=args.force_enrich)