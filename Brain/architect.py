"""Dragon Architect - İlk board yapısını oluştur"""
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_PATH = os.path.join(BASE_DIR, "Archive")
BOARD_DATA_FILE = os.path.join(ARCHIVE_PATH, "dragon_board.json")

class DragonArchitect:
    """Board yapısını tasarla ve oluştur"""
    
    def __init__(self):
        if not os.path.exists(ARCHIVE_PATH):
            os.makedirs(ARCHIVE_PATH)
            logger.info(f"Archive klasörü oluşturuldu: {ARCHIVE_PATH}")
        
        self.data = {"tasks": [], "logs": []}
        
        # Varsa mevcut board'u yükle
        if os.path.exists(BOARD_DATA_FILE):
            try:
                with open(BOARD_DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Mevcut board yüklendi: {len(self.data.get('tasks', []))} görev")
            except json.JSONDecodeError:
                logger.warning("Board JSON bozuk, yeni yapı oluşturuluyor")
                self.data = {"tasks": [], "logs": []}

    def create_task(self, title, lang, desc, status="todo"):
        """Yeni görev oluştur"""
        # Dil doğrulaması
        valid_langs = ["C# (Unity)", "Java (Sistem)", "Python (AI)"]
        if lang not in valid_langs:
            logger.error(f"Geçersiz dil: {lang}. Desteklenen: {', '.join(valid_langs)}")
            return False
        
        if not title or not title.strip():
            logger.error("Başlık boş olamaz")
            return False
        
        task = {
            "id": len(self.data["tasks"]) + 1,
            "title": title.strip(),
            "language": lang,
            "description": desc.strip() if desc else "",
            "status": status,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["tasks"].append(task)
        self.save_to_archive()
        logger.info(f"✅ Görev oluşturuldu: {title}")
        return True

    def save_to_archive(self):
        """Board'u dosyaya kaydet"""
        try:
            with open(BOARD_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            logger.info(f"✅ Board kaydedildi: {BOARD_DATA_FILE}")
            return True
        except IOError as e:
            logger.error(f"Kayıt hatası: {e}")
            return False

if __name__ == "__main__":
    # Örnek kullanım
    architect = DragonArchitect()
    architect.create_task("Giriş Sistemi", "Java (Sistem)", "Kullanıcı giriş loglarını tutan yapı")
    architect.create_task("FPS Silah Sistemi", "C# (Unity)", "Oyuncu silah mekanikleri ve animasyonları")
    architect.create_task("AI Pathfinding", "Python (AI)", "Yapay zeka düşman hareket algoritmaları")