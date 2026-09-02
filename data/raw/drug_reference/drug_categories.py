"""
İlaç Kategori Haritası
-----------------------
CATEGORY_MAP: Etkin madde -> klinik kategori
DOSAGE_TYPE_MAP: Klinik kategori -> skorlama tipi
PEDIATRIK_SURUP_MAP: Çocuk şurupları için formülasyon bazlı ayrı doz haritası
"""

CATEGORY_MAP = {

    "PARASETAMOL": "Ağrı Kesici", "DEKSKETOPROFEN": "Ağrı Kesici", "İBUPROFEN": "Ağrı Kesici",
    "FLURBİPROFEN": "Ağrı Kesici", "NAPROKSEN": "Ağrı Kesici", "ASETİLSALİSİLİK ASİT": "Ağrı Kesici",
    "DİKLOFENAK": "Ağrı Kesici", "MELOKSİKAM": "Ağrı Kesici", "ETODOLAK": "Ağrı Kesici", "KETOPROFEN": "Ağrı Kesici",


    "AMOKSİSİLİN": "Antibiyotik", "MOKSİFLOKSASİN": "Antibiyotik", "SEFAZOLİN": "Antibiyotik",
    "AZİTROMİSİN": "Antibiyotik", "SEFUROKSİM": "Antibiyotik", "SİPROFLOKSASİN": "Antibiyotik",
    "LEVOFLOKSASİN": "Antibiyotik", "KLARİTROMİSİN": "Antibiyotik", "FOSFOMİSİN": "Antibiyotik", "SEFTRİAKSON": "Antibiyotik",


    "METFORMİN": "Diyabet", "GLİKLAZİD": "Diyabet", "GLİMEPİRİD": "Diyabet",
    "VİLDAGLİPTİN": "Diyabet", "SİTAGLİPTİN": "Diyabet", "PİOGLİTAZON": "Diyabet", "İNSÜLİN": "Diyabet",


    "VERAPAMİL": "Kalp/Tansiyon", "KANDESARTAN": "Kalp/Tansiyon", "AMLODİPİN": "Kalp/Tansiyon",
    "METOPROLOL": "Kalp/Tansiyon", "RAMİPRİL": "Kalp/Tansiyon", "VALSARTAN": "Kalp/Tansiyon",
    "PERİNDOPRİL": "Kalp/Tansiyon", "HİDROKLOROTİYAZİD": "Kalp/Tansiyon", "DİLTİAZEM": "Kalp/Tansiyon",
    "ATORVASTATİN": "Kolesterol", "ROSUVASTATİN": "Kolesterol",


    "LEVOTİROKSİN": "Tiroid",


    "DOKSORUBİSİN": "Onkoloji", "REGORAFENİB": "Onkoloji", "ASCİMİNİB": "Onkoloji",
    "TAMOKSİFEN": "Onkoloji", "İMATİNİB": "Onkoloji", "KAPESİTABİN": "Onkoloji",
    "RİTUKSİMAB": "Onkoloji", "TRASTUZUMAB": "Onkoloji", "KARBOPLATİN": "Onkoloji",
    "SİSPLATİN": "Onkoloji", "PAKLİTAKSEL": "Onkoloji", "FLOROURASİL": "Onkoloji",


    "PANTOPRAZOL": "Mide", "LANSOPRAZOL": "Mide", "ESOMEPRAZOL": "Mide", "RABEPRAZOL": "Mide",
    "OMEPRAZOL": "Mide", "FAMOTİDİN": "Mide", "SİMETİKON": "Mide",


    "İPRATROPİUM": "Solunum", "SALBUTAMOL": "Solunum-PRN", "BUDESONİD": "Solunum",
    "FORMOTEROL": "Solunum", "MONTELUKAST": "Solunum", "FLUTİKAZON": "Solunum",


    "NİRMATRELVİR": "Antiviral", "RİTONAVİR": "Antiviral", "OSELTAMİVİR": "Antiviral", "ASİKLOVİR": "Antiviral",


    "LEVETİRASETAM": "Sinir Sistemi", "PREGABALİN": "Sinir Sistemi-Bağımlılık Riskli", "GABAPENTİN": "Sinir Sistemi-Bağımlılık Riskli",
    "ESSİTALOPRAM": "Psikiyatri", "SERTRALİN": "Psikiyatri",

  
    "ALPRAZOLAM": "Anksiyolitik/Uyku-Bağımlılık Riskli", "ZOLPİDEM": "Anksiyolitik/Uyku-Bağımlılık Riskli", "DİAZEPAM": "Anksiyolitik/Uyku-Bağımlılık Riskli",



    "SUMATRİPTAN": "Migren", "KSİLOMETAZOLİN": "Nazal Dekonjestan", "OKSİMETAZOLİN": "Nazal Dekonjestan",
    "LOPERAMİD": "Antidiyareik", "METOKLOPRAMİD": "Antiemetik"
}

DOSAGE_TYPE_MAP = {
    "Ağrı Kesici": "TIP1_GECICI", "Migren": "TIP1_GECICI", "Nazal Dekonjestan": "TIP1_GECICI",
    "Antidiyareik": "TIP1_GECICI", "Antiemetik": "TIP1_GECICI", "Solunum-PRN": "TIP1_GECICI",
    "Anksiyolitik/Uyku-Bağımlılık Riskli": "TIP1_GECICI", "Antibiyotik": "TIP1_GECICI",
    "Antiviral": "TIP1_GECICI", "Mide": "TIP1_GECICI",
    "Diyabet": "TIP2_KRONIK", "Kalp/Tansiyon": "TIP2_KRONIK", "Kolesterol": "TIP2_KRONIK",
    "Tiroid": "TIP2_KRONIK", "Onkoloji": "TIP2_KRONIK", "Solunum": "TIP2_KRONIK",
    "Sinir Sistemi": "TIP2_KRONIK", "Sinir Sistemi-Bağımlılık Riskli": "TIP2_KRONIK", "Psikiyatri": "TIP2_KRONIK",
}

PEDIATRIK_SURUP_MAP = {
    "PARASETAMOL_SURUP": {
        "ornek_marka": "Calpol / Minoset Pediatrik",
        "konsantrasyon_mg_per_5ml": 120,
        "mg_kg_doz_araligi": (10, 15),
        "gunluk_maks_doz_sayisi": 4,
        "kategori": "Ağrı Kesici"
    },
    "İBUPROFEN_SURUP": {
        "ornek_marka": "Dolven / İbufen",
        "konsantrasyon_mg_per_5ml": 100,
        "mg_kg_doz_araligi": (5, 10),
        "gunluk_maks_doz_sayisi": 3,
        "kategori": "Ağrı Kesici"
    },
    "AMOKSİSİLİN_SURUP": {
        "ornek_marka": "Augmentin / Klamoks / Croxilex", 
        "konsantrasyon_mg_per_5ml": 400, 
        "mg_kg_doz_araligi": (25, 45), 
        "gunluk_maks_doz_sayisi": 2, 
        "kategori": "Antibiyotik"
    },
    "KLARİTROMİSİN_SURUP": {
        "ornek_marka": "Macrol / Klacid",
        "konsantrasyon_mg_per_5ml": 125, 
        "mg_kg_doz_araligi": (7.5, 15), 
        "gunluk_maks_doz_sayisi": 2,
        "kategori": "Antibiyotik"
    },
    "SEFUROKSİM_SURUP": {
        "ornek_marka": "Zinnat / Aksef",
        "konsantrasyon_mg_per_5ml": 125,
        "mg_kg_doz_araligi": (10, 15),
        "gunluk_maks_doz_sayisi": 2,
        "kategori": "Antibiyotik"
    },
    "AZİTROMİSİN_SURUP": {
        "ornek_marka": "Zitromax / Azitro",
        "konsantrasyon_mg_per_5ml": 200,
        "mg_kg_doz_araligi": (10, 12), 
        "gunluk_maks_doz_sayisi": 1,
        "kategori": "Antibiyotik"
    }
}