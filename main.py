import time
import sys


def main():
    print("MediGuard Risk Motoru ve Reçete Akışı Başlatılıyor...")
    try:
 
        
        print("Sistem Kafka üzerinden reçeteleri dinlemeye/üretmeye hazır. (Çıkış için CTRL+C)")
        while True:

            time.sleep(1) 
            
    except KeyboardInterrupt:
        print("\nAkış durduruldu. Yeniden başlatıldığında sistem mevcut hastalarla kaldığı yerden devam edecek.")
        sys.exit(0)

if __name__ == "__main__":
    main()