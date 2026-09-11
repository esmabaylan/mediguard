import threading
import time
import sys

from src.data_generation.prescription_generator import start_generating_prescriptions
from src.streaming.prescription_consumer import start_prescription_consumer
from src.streaming.db_writer import start_db_writer
from src.utils.logger import run_with_error_logging, logger

if __name__ == "__main__":
    logger.info("MediGuard Merkezi Yonetim Sistemi Baslatiliyor...")
    

    writer_thread = threading.Thread(
        target=run_with_error_logging, 
        args=(start_db_writer, "DB_WRITER"),
        daemon=True
    )
    writer_thread.start()
    time.sleep(1)
    

    risk_thread = threading.Thread(
        target=run_with_error_logging, 
        args=(start_prescription_consumer, "RISK_ENGINE"),
        daemon=True
    )
    risk_thread.start()
    time.sleep(1)
    

    producer_thread = threading.Thread(
        target=run_with_error_logging, 
        args=(start_generating_prescriptions, "PRODUCER"),
        daemon=True
    )
    producer_thread.start()

    logger.info("Tum servisler tek terminal altinda basariyla ayaklandi. (Cikmak icin CTRL+C)")
    print("-" * 65)

    try:

        while True:
            time.sleep(5)
            if not writer_thread.is_alive():
                logger.warning("DB_WRITER servisi su an calismiyor!")
            if not risk_thread.is_alive():
                logger.warning("RISK_ENGINE servisi su an calismiyor!")
            if not producer_thread.is_alive():
                logger.warning("PRODUCER servisi su an calismiyor!")
                
    except KeyboardInterrupt:
        logger.info("Sistem kullanici tarafindan kapatiliyor. Tum servisler durduruldu.")
        sys.exit(0)