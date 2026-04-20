import json
import os
import requests # İnternetten ganimet toplamak için

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
        chars = {"ç": "c", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ı": "i", "İ": "I"}
        for tr, en in chars.items():
            text = text.replace(tr, en)
        return text.replace(" ", "_").lower()

    def download_preview(self, keyword, folder):
        # Görevin ismine göre internetten sembolik bir görsel çeker
        # source.unsplash.com artık direkt keyword kabul ediyor
        img_url = f"https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=400" # Örnek teknoloji görseli
        try:
            # Not: Gerçek API anahtarı olmadan rastgele çekmek için statik bir placeholder da kullanılabilir
            response = requests.get(img_url, timeout=5)
            if response.status_code == 200:
                with open(os.path.join(folder, "preview.jpg"), 'wb') as f:
                    f.write(response.content)
                return True
        except:
            return False
        return False
    
    def generate_workshop_code(self, task_title, lang):
        # Workshop klasör yolunu belirle
        WORKSHOP_PATH = os.path.join(BASE_DIR, "Workshop")
        if not os.path.exists(WORKSHOP_PATH):
            os.makedirs(WORKSHOP_PATH)
        
        file_name = self.turkish_to_english(task_title)
        
        # Dil bazlı taslak seçimi
        if "C#" in lang:
            ext = ".cs"
            code = f"using UnityEngine;\n\npublic class {task_title.replace(' ', '')} : MonoBehaviour\n{{\n    void Start()\n    {{\n        Debug.Log('🐉 Dragon Eye: {task_title} sistemi aktif.');\n    }}\n}}"
        elif "Java" in lang:
            ext = ".java"
            code = f"public class {task_title.replace(' ', '')} {{\n    public static void main(String[] args) {{\n        System.out.println(\"🐉 Dragon System: {task_title} baslatildi.\");\n    }}\n}}"
        else:
            return # Diğer diller için şimdilik pas geç

        # Dosyayı Workshop klasörüne yaz
        file_path = os.path.join(WORKSHOP_PATH, file_name + ext)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"🛠️ {task_title} için kod taslağı Workshop'a fırlatıldı.")

    def scan_board_and_find_refs(self):
        if not os.path.exists(BOARD_FILE):
            print("❌ Hata: dragon_board.json bulunamadı!")
            return

        with open(BOARD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for task in data["tasks"]:
            keyword = task["title"]
            clean_folder_name = self.turkish_to_english(keyword)
            ref_folder = os.path.join(REF_PATH, clean_folder_name)
            
            if not os.path.exists(ref_folder):
                print(f"👁️ Dragon Scout Gözlemliyor: {keyword} için klasör ve ganimet hazırlanıyor...")
                os.makedirs(ref_folder)
                self.generate_workshop_code(keyword, task["language"])
                
                # Git takibi için .gitkeep
                with open(os.path.join(ref_folder, ".gitkeep"), "w") as f:
                    f.write("")
                
                # Referans Logu
                with open(os.path.join(ref_folder, "ref_log.txt"), "w", encoding='utf-8') as log:
                    log.write(f"{keyword} görevi için Dragon Scout tarafından oluşturuldu.\n")
                
                # Görsel Ganimet
                if self.download_preview(keyword, ref_folder):
                    print(f"📸 {keyword} için önizleme görseli indirildi.")
                
        print("✅ Dragon Scout taramayı tamamladı.")

if __name__ == "__main__":
    scout = DragonScout()
    scout.scan_board_and_find_refs()