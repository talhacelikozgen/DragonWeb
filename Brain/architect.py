import json
import os

# Klasör yollarını senin ana repona (DragonWeb) göre ayarladık
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_PATH = os.path.join(BASE_DIR, "Archive")
BOARD_DATA_FILE = os.path.join(ARCHIVE_PATH, "dragon_board.json")

class DragonArchitect:
    def __init__(self):
        # Eğer Archive klasörü yoksa oluştur
        if not os.path.exists(ARCHIVE_PATH):
            os.makedirs(ARCHIVE_PATH)
        
        self.data = {"tasks": [], "logs": []}

    def create_task(self, title, lang, desc):
        task = {
            "title": title,
            "language": lang,
            "description": desc,
            "status": "todo"
        }
        self.data["tasks"].append(task)
        self.save_to_archive()

    def save_to_archive(self):
        with open(BOARD_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        print(f"✅ Görev kaydedildi: {BOARD_DATA_FILE}")

# Kullanım
architect = DragonArchitect()
architect.create_task("Giriş Sistemi", "Java", "Kullanıcı giriş loglarını tutan yapı")