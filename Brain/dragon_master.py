import subprocess
import time
import sys
import os

def run_git_sync():
    # Otomatik Git Push Komutu
    try:
        subprocess.run(["git", "add", "."], check=True)
        # Sadece değişiklik varsa commit at
        status = subprocess.check_output(["git", "status", "--porcelain"])
        if status:
            subprocess.run(["git", "commit", "-m", "🐉 Dragon Archive: Otomatik Senkronizasyon"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("🚀 Dragon Archive GitHub'a fırlatıldı!")
    except Exception as e:
        print(f"⚠️ Git Sync Hatası: {e}")

def run_system():
    print("🐉 Dragon Brain Uyandırılıyor...")
    server_process = subprocess.Popen([sys.executable, "Brain/server.py"])
    
    try:
        while True:
            print("👁️ Dragon Scout devriyeye çıkıyor...")
            subprocess.run([sys.executable, "Brain/scout.py"])
            
            # Her taramadan sonra Git'e yolla
            run_git_sync()
            
            time.sleep(60) 
    except KeyboardInterrupt:
        server_process.terminate()

if __name__ == "__main__":
    run_system()