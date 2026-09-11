from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import os
import re

from src.utils.logger import logger

def categorize_drug_by_ingredient(active_ingredient_text):
    if not active_ingredient_text:
        return "Belirsiz"
        
    ingredient_upper = str(active_ingredient_text).upper()
    
    CATEGORY_MAP = {
        "PARASETAMOL": "Ağrı Kesici", "DEKSKETOPROFEN": "Ağrı Kesici", "İBUPROFEN": "Ağrı Kesici",
        "FLURBİPROFEN": "Ağrı Kesici", "NAPROKSEN": "Ağrı Kesici", "ASETİLSALİSİLİK ASİT": "Ağrı Kesici",
        "DİKLOFENAK": "Ağrı Kesici", "MELOKSİKAM": "Ağrı Kesici", "ETODOLAK": "Ağrı Kesici", "KETOPROFEN": "Ağrı Kesici",
        

        "AMOKSİSİLİN": "Antibiyotik", "MOKSİFLOKSASİN": "Antibiyotik", "SEFAZOLİN": "Antibiyotik",
        "AZİTROMİSİN": "Antibiyotik", "SEFUROKSİM": "Antibiyotik", "SİPROFLOKSASİN": "Antibiyotik",
        "LEVOFLOKSASİN": "Antibiyotik", "KLARİTROMİSİN": "Antibiyotik", "FOSFOMİSİN": "Antibiyotik", "SEFTRİAKSON": "Antibiyotik",
        

        "METFORMİN": "Diyabet", "GLİKLAZİD": "Diyabet", "GLİMEPİRİD": "Diyabet", "VİLDAGLİPTİN": "Diyabet",
        "SİTAGLİPTİN": "Diyabet", "PİOGLİTAZON": "Diyabet", "İNSÜLİN": "Diyabet",
        
        "VERAPAMİL": "Kalp/Tansiyon", "KANDESARTAN": "Kalp/Tansiyon", "AMLODİPİN": "Kalp/Tansiyon",
        "METOPROLOL": "Kalp/Tansiyon", "RAMİPRİL": "Kalp/Tansiyon", "VALSARTAN": "Kalp/Tansiyon",
        "PERİNDOPRİL": "Kalp/Tansiyon", "HİDROKLOROTİYAZİD": "Kalp/Tansiyon", "DİLTİAZEM": "Kalp/Tansiyon",
        "ATORVASTATİN": "Kolesterol", "ROSUVASTATİN": "Kolesterol",
        
        "PANTOPRAZOL": "Mide", "LANSOPRAZOL": "Mide", "ESOMEPRAZOL": "Mide", "RABEPRAZOL": "Mide",
        "OMEPRAZOL": "Mide", "FAMOTİDİN": "Mide", "SİMETİKON": "Mide",
        
        "İPRATROPİUM": "Solunum", "SALBUTAMOL": "Solunum", "BUDESONİD": "Solunum",
        "FORMOTEROL": "Solunum", "MONTELUKAST": "Solunum", "FLUTİKAZON": "Solunum",
        
        "NİRMATRELVİR": "Antiviral", "RİTONAVİR": "Antiviral", "OSELTAMİVİR": "Antiviral", "ASİKLOVİR": "Antiviral",
        
        "LEVETİRASETAM": "Sinir Sistemi", "PREGABALİN": "Sinir Sistemi", "GABAPENTİN": "Sinir Sistemi",
        "ESSİTALOPRAM": "Psikiyatri", "SERTRALİN": "Psikiyatri",

        "DOKSORUBİSİN": "Onkoloji","REGORAFENİB": "Onkoloji","ASCİMİNİB": "Onkoloji",
        "TAMOKSİFEN": "Onkoloji","İMATİNİB": "Onkoloji",
        "KAPESİTABİN": "Onkoloji","RİTUKSİMAB": "Onkoloji","TRASTUZUMAB": "Onkoloji",
        "KARBOPLATİN": "Onkoloji","SİSPLATİN": "Onkoloji","PAKLİTAKSEL": "Onkoloji","FLOROURASİL": "Onkoloji"
    }
    
    for keyword, category in CATEGORY_MAP.items():
        if keyword in ingredient_upper:
            return category
            
    return "Diğer / Sınıflandırılamadı"

def parse_titck_table(target_url="https://titck.gov.tr/kubkt"):
    csv_file = "data/titck_drugs_extracted.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ["drug_name", "active_ingredient", "category"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()

        chrome_options = Options()
        

        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("TİTCK sayfası yükleniyor...")
        driver.get(target_url)
        

        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "posts_length")))
            select = Select(driver.find_element(By.NAME, "posts_length"))
            select.select_by_value("100")
            logger.info("Sayfa başına kayıt sayısı 100 olarak ayarlandı. Hızlandırılıyor...")
            time.sleep(3)
        except Exception as e:
            logger.error("Kayıt sayısı değiştirilemedi:", e)
        
        current_page = 1
        
        while True:
            logger.info(f"\n--- Sayfa {current_page} İşleniyor ---")
            
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "posts")))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.find_all('tr', class_=re.compile(r'table-row'))
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 7:
                    continue
                    
                drug_name = cols[0].text.strip()
                active_ingredient = cols[1].text.strip()
                category = categorize_drug_by_ingredient(active_ingredient)
                
                writer.writerow({
                    "drug_name": drug_name,
                    "active_ingredient": active_ingredient,
                    "category": category
                })
                
            f.flush()
            logger.info(f"Sayfa {current_page} tamamlandı. ({len(rows)} ilaç kaydedildi)")
                

            clicked = False
            for attempt in range(3):
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "posts_next"))
                    )
                    
                    if "disabled" in next_button.get_attribute("class"):
                        logger.info("\nSon sayfaya ulaşıldı, tüm veriler başarıyla çekildi.")
                        clicked = True
                        break
                        
                    driver.execute_script("arguments[0].click();", next_button)
                    current_page += 1
                    clicked = True
                    time.sleep(2) 
                    break 
                    
                except Exception as e:
                    logger.error(f"Sayfa geçişi yenileniyor (Deneme {attempt+1}/3): {e}")
                    time.sleep(2)
                    
            if not clicked:
                logger.error("Maksimum deneme aşıldı, sonraki sayfaya geçilemiyor.")
                break
                
        driver.quit()

if __name__ == "__main__":
    parse_titck_table()