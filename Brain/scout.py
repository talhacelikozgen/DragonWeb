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

    def turkish_to_english(self, text):
        # Türkçe karakterleri link ve dosya dostu hale getirir
        chars = {"ç": "c", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ı": "i", "İ": "I"}
        for tr, en in chars.items():
            text = text.replace(tr, en)
        return text.replace(" ", "_").lower()

    def scan_board_and_find_refs(self):
        if not os.path.exists(BOARD_FILE):
            print("❌ Hata: dragon_board.json bulunamadı!")
            return

        with open(BOARD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for task in data["tasks"]:
            keyword = task["title"]
            clean_folder_name = self.turkish_to_english(keyword)
            print(f"👁️ Dragon Scout Gözlemliyor: {keyword} için referans aranıyor...")
            
            ref_folder = os.path.join(REF_PATH, clean_folder_name)
            
            if not os.path.exists(ref_folder):
                os.makedirs(ref_folder)
                # .gitkeep ekliyoruz ki Git klasörü boş olsa da GitHub'a göndersin
                with open(os.path.join(ref_folder, ".gitkeep"), "w") as f:
                    f.write("")
                
                with open(os.path.join(ref_folder, "ref_log.txt"), "w", encoding='utf-8') as log:
                    log.write(f"{keyword} için ganimetler burada toplanacak.")
        
        print("✅ Dragon Scout taramayı tamamladı. Ganimetler Archive/References altında.")

if __name__ == "__main__":
    scout = DragonScout()
    scout.scan_board_and_find_refs()