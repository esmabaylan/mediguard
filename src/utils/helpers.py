import random

FEMALE_NAMES = [
    "Ayşe", "Fatma", "Zeynep", "Elif", "Esma", "Nuray", "Betül", "Merve",
    "Büşra", "Kübra", "Ceren", "Gizem", "Selin", "Eda", "Melis", "Tuğba",
    "Yasemin", "Derya", "Deniz", "Eylül", "Doğa", "Cansu", "İrem", "Aslı",
    "Emine", "Hatice", "Havva", "Zehra", "Sultan", "Şule", "Gül", "Gülcan",
    "Gülsüm", "Hülya", "Nur", "Nurcan", "Nurten", "Songül", "Sevgi", "Sevil",
    "Sevim", "Sibel", "Filiz", "Funda", "Aylin", "Arzu", "Aysun", "Ayten",
    "Ayla", "Ebru", "Emel", "Esra", "Fadime", "Fulya", "Gamze", "Gonca",
    "Gülay", "Gülden", "Handan", "Hilal", "Hümeyra", "İlknur", "Kadriye",
    "Kevser", "Leyla", "Meltem", "Meryem", "Neslihan", "Nesrin", "Nihal",
    "Nilay", "Nilgün", "Oya", "Özge", "Özlem", "Pelin", "Pınar", "Rabia",
    "Rukiye", "Saadet", "Seda", "Selma", "Semra", "Serap", "Serpil", "Sevda",
    "Şeyma", "Şükran", "Tülay", "Tülin", "Ümmü", "Yeliz", "Yıldız", "Zuhal",
    "Zübeyde", "Asiye", "Bahar", "Belgin", "Berna", "Beyza", "Canan", "Damla",
    "Duygu", "Dilara", "Dilek", "Ece", "Ecrin", "Elvan", "Feride", "Ferah",
    "Gülnaz", "Işıl", "Işın", "Kader", "Kamile", "Lale", "Melike", "Nazlı",
    "Perihan", "Reyhan", "Sedef", "Sinem", "Şeyda", "Ülkü", "Yağmur", "Zerrin"
]
 
MALE_NAMES = [
    "Ahmet", "Mehmet", "Mustafa", "Ali", "Hasan", "Hüseyin", "Can", "Burak",
    "Altuğ", "Şakir", "Emre", "Onur", "Oğuzhan", "Kerem", "Yunus", "Efe",
    "Enes", "Kaan", "Umut", "Volkan", "Hakan", "Yasin", "Ozan", "Gökhan",
    "İbrahim", "İsmail", "Osman", "Yusuf", "Murat", "Serkan", "Cem", "Cemal",
    "Cengiz", "Erdem", "Erhan", "Ergün", "Fatih", "Fikret", "Furkan", "Halil",
    "Harun", "İlker", "İrfan", "Kadir", "Kemal", "Kenan", "Levent", "Mahmut",
    "Metin", "Muhammet", "Necati", "Necmettin", "Nihat", "Nuri", "Nurettin",
    "Orhan", "Orkun", "Recep", "Reşat", "Rıdvan", "Rıza", "Sabri", "Sadık",
    "Salih", "Selim", "Serdar", "Sinan", "Süleyman", "Şaban", "Taner", "Tarık",
    "Tayfun", "Tolga", "Tufan", "Turgay", "Turgut", "Ufuk", "Vedat", "Veli",
    "Yakup", "Yavuz", "Zafer", "Adem", "Adnan", "Akın", "Alper", "Anıl",
    "Arda", "Aziz", "Barış", "Baran", "Batuhan", "Berk", "Bertan", "Bora",
    "Bülent", "Cevdet", "Çağatay", "Çağlar", "Ege", "Ekrem", "Erkan", "Faruk",
    "Galip", "Gürkan", "Işık", "İzzet", "Koray", "Mert", "Nail", "Necip",
    "Nedim", "Ramazan", "Samet", "Semih", "Talha", "Taha", "Uğur", "Yiğit"
]
 
LAST_NAMES = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Öztürk", "Aydın",
    "Özdemir", "Arslan", "Baylan", "Dokuz", "Doğan", "Kılıç", "Aslan", "Çetin",
    "Kara", "Koç", "Güneş", "Bulut", "Bozkurt", "Avcı", "Er", "Köse",
    "Şimşek", "Aksoy", "Aktaş", "Erdoğan", "Güler", "Öz", "Polat", "Korkmaz",
    "Özkan", "Çakır", "Yalçın", "Uçar", "Duman", "Kurt", "Turan", "Acar",
    "Işık", "Bilgin", "Sarı", "Çakmak", "Karataş", "Yavuz", "Ateş", "Kaplan",
    "Tekin", "Uzun", "Gündoğdu", "Ekinci", "Erkan", "Bayram", "Çiçek", "Toprak",
    "Şen", "Aydemir", "Genç", "Bal", "Gül", "Coşkun", "Doğru", "Karaca",
    "Yücel", "Aksu", "Baş", "Yurt", "Sezer", "Değirmenci", "Sağlam", "Türk",
    "Balcı", "Ergin", "Bekar", "Sönmez", "Küçük", "Büyük", "Ünal", "Işıklar",
    "Karadağ", "Boz", "Tan", "Aygün", "Çevik", "Erol", "Görgün", "Karagöz",
    "Onat", "Öner", "Özcan", "Öztaş", "Sancak", "Solmaz", "Taş", "Yaman",
    "Yazıcı", "Yenigün", "Zengin", "Akkaya", "Akan", "Alkan", "Ay", "Aybar",
    "Bahadır", "Baltacı", "Başaran", "Ceylan", "Çobanoğlu", "Erbay", "Gökçe",
    "Gürsoy", "Kutlu", "Özay", "Özsoy", "Tunç", "Uysal", "Yaşar", "Yıldırım"
]


def generate_mock_person() -> tuple:
    """Önce cinsiyeti belirler, ardından uygun havuzdan ad ve rastgele soyad döndürür."""
    gender = random.choice(["E", "K"])
    first_name = random.choice(MALE_NAMES) if gender == "E" else random.choice(FEMALE_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    return gender, first_name, last_name
def generate_mock_tckn() -> str:
    """Turkiye Cumhuriyeti algoritmasina tam uyumlu, gecerli bir TCKN uretir."""
    tc = [0] * 11
    
    tc[0] = random.randint(1, 9)
    
    
    for i in range(1, 9):
        tc[i] = random.randint(0, 9)
        

    sum_odd = tc[0] + tc[2] + tc[4] + tc[6] + tc[8]  
    sum_even = tc[1] + tc[3] + tc[5] + tc[7]        
    
    
    tc[9] = ((sum_odd * 7) - sum_even) % 10
    
    tc[10] = sum(tc[:10]) % 10
    
    return ''.join(map(str, tc))