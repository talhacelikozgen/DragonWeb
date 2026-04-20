"""Dragon Master - Scout'u yönetme ve koordinasyon"""
import sys
import os

# Scout modülünü import et
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scout import DragonScout
import logging

logger = logging.getLogger(__name__)

class DragonMaster:
    """Scout'u orkestrasyonla yönet"""
    
    def __init__(self):
        self.scout = DragonScout()
    
    def run_operations(self):
        """Tüm Dragon operasyonlarını çalıştır"""
        logger.info("🐉 Dragon Master başlatıldı")
        success = self.scout.scan_board_and_find_refs()
        if success:
            logger.info("✅ Tüm operasyonlar başarıyla tamamlandı")
            return True
        else:
            logger.warning("⚠️ Bazı operasyonlar başarısız olmuş olabilir")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    master = DragonMaster()
    success = master.run_operations()
    sys.exit(0 if success else 1)