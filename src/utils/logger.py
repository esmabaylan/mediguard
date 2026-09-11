import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("mediguard")

def run_with_error_logging(target_func, name):
    """
    Alt servislerde (thread) oluşan hataları yakalayıp detaylı loglayan sarmalayıcı.
    """
    try:
        logger.info(f"[{name}] Servisi baslatiliyor...")
        target_func()
    except Exception as e:
        logger.critical(f"[{name}] Servisi coktu! Hata detaylari: {str(e)}", exc_info=True)