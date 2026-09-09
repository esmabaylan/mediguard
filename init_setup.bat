@echo off
echo [1/4] Docker konteynerleri ayaga kaldiriliyor...
docker-compose up -d

echo [2/4] PostgreSQL'in hazir olmasi bekleniyor (10 saniye)...
timeout /t 10 /nobreak >nul

echo [3/4] Ilac referans verileri veritabanina yukleniyor...
docker exec -it mediscope_core python -m src.reference.drug_reference_loader

echo [4/4] Sentetik hasta verileri uretiliyor...
docker exec -it mediscope_core python -m src.data_generation.patient_generator

echo Kurulum tamamlandi! Sistem gercek zamanli akisa hazir.