import subprocess
import time
import sys
import os

def run_system():
    print("🐉 Dragon Brain Uyandırılıyor...")
    
    # 1. Server.py'yi arka planda (ayrı bir işlem olarak) başlat
    # Bu sayede server sürekli açık kalır
    server_process = subprocess.Popen([sys.executable, "Brain/server.py"])
    print("📡 Dragon Server (Dinleyici) Aktif.")

    try:
        while True:
            # 2. Scout.py'yi her 60 saniyede bir otomatik çalıştır
            # Yeni görev gelmişse klasörleri açar
            print("👁️ Dragon Scout devriyeye çıkıyor...")
            subprocess.run([sys.executable, "Brain/scout.py"])
            
            # 60 saniye bekle (bu süreyi ihtiyacına göre değiştirebilirsin)
            time.sleep(60) 
            
    except KeyboardInterrupt:
        print("\n🐉 Dragon Brain uyku moduna geçiyor...")
        server_process.terminate() # Server'ı kapat

if __name__ == "__main__":
    run_system()