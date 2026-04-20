"""Dragon Master - Scout'u yönetme ve koordinasyon"""
import sys
import os
import time
import subprocess
import logging

# Scout modülünü import et
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scout import DragonScout

logger = logging.getLogger(__name__)

class DragonMaster:
    """Scout'u orkestrasyonla yönet ve Server'ı canlı tut"""
    
    def __init__(self):
        self.scout = DragonScout()
        self.server_process = None

    def start_server(self):
        """API Server'ı arka planda başlat"""
        python_exe = sys.executable
        server_path = os.path.join(BASE_DIR, "Brain", "server.py")
        logger.info("📡 Dragon Server (API) arka planda başlatılıyor...")
        self.server_process = subprocess.Popen([python_exe, server_path])
        time.sleep(2) # Server'ın kendine gelmesi için süre

    def run_operations(self):
        """Sürekli döngüde operasyonları yönet"""
        logger.info("🐉 Dragon Master operasyon odasına girdi.")
        
        # 1. Server'ı aç
        self.start_server()

        try:
            while True:
                logger.info("👁️ Dragon Scout devriyeye çıkıyor...")
                success = self.scout.scan_board_and_find_refs()
                
                if success:
                    # Otomatik Git Push (Opsiyonel)
                    os.system("git add .")
                    os.system('git commit -m "🐉 Dragon Auto-Sync" & git push origin main')
                    logger.info("✅ Devriye tamamlandı, veriler senkronize.")
                
                logger.info("⏳ 60 saniye dinlenme (Kapatmak için CTRL+C)...")
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("🐉 Dragon Master uyku moduna geçiyor...")
        finally:
            if self.server_process:
                self.server_process.terminate()
                logger.info("📡 Server kapatıldı.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    master = DragonMaster()
    master.run_operations()