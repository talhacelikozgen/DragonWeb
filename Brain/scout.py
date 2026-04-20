import json
import os

# Yolları belirle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_PATH = os.path.join(BASE_DIR, "Archive")
REF_PATH = os.path.join(ARCHIVE_PATH, "References")
BOARD_FILE = os.path.join(ARCHIVE_PATH, "dragon_board.json")

class DragonScout:
    def __init__(self):
        if not os.path.exists(REF_PATH):
            os.makedirs(REF_PATH)

    def scan_board_and_find_refs(self):
        with open(BOARD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for task in data["tasks"]:
            keyword = task["title"]
            print(f"👁️ Dragon Scout Gözlemliyor: {keyword} için referans aranıyor...")
            
            # Burada internetten veri çekme simülasyonu yapıyoruz
            # İleride burası otomatik resim/kod indirecek
            ref_folder = os.path.join(REF_PATH, keyword.replace(" ", "_"))
            if not os.path.exists(ref_folder):
                os.makedirs(ref_folder)
                with open(os.path.join(ref_folder, "ref_log.txt"), "w") as log:
                    log.write(f"{keyword} için referanslar buraya toplanacak.")
        
        print("✅ Dragon Scout taramayı tamamladı. Ganimetler Archive/References altında.")

# Çalıştır
scout = DragonScout()
scout.scan_board_and_find_refs()