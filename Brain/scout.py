import json
import os
import requests
import logging
import random
from datetime import datetime

# Logging ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Yolları belirle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_PATH = os.path.join(BASE_DIR, "Archive")
REF_PATH = os.path.join(ARCHIVE_PATH, "References")
BOARD_FILE = os.path.join(ARCHIVE_PATH, "dragon_board.json")
WORKSHOP_PATH = os.path.join(BASE_DIR, "Workshop")

class DragonScout:
    def __init__(self):
        # Gerekli klasörleri oluştur
        for path in [REF_PATH, WORKSHOP_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info(f"📁 Klasör oluşturuldu: {path}")

    def clean_name(self, text):
        """Türkçe karakterleri temizler ve dosya dostu isim yapar"""
        if not text: return "isimsiz_gorev"
        tr_map = {"ç": "c", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ı": "i", "İ": "I", 
                  "Ç": "C", "Ş": "S", "Ğ": "G", "Ü": "U", "Ö": "O"}
        for tr, en in tr_map.items():
            text = text.replace(tr, en)
        return text.replace(" ", "_").lower().strip()

    def download_preview(self, keyword, folder):
        """Görseli indirir ve klasöre kaydeder"""
        random_id = random.randint(1, 1000)
        # Unsplash bazen Türkçe karakterde sorun yaşayabilir, keyword'ü temizleyelim
        search_term = keyword.replace(" ", ",")
        search_url = f"https://source.unsplash.com/featured/400x300?{search_term},robot,game&sig={random_id}"
        
        try:
            response = requests.get(search_url, timeout=15, allow_redirects=True)
            if response.status_code == 200:
                file_full_path = os.path.join(folder, "preview.jpg")
                with open(file_full_path, 'wb') as f:
                    f.write(response.content)
                # KESİN LOG:
                logger.info(f"📸 GÖRSEL KAYDEDİLDİ: {file_full_path}")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Görsel Hatası: {e}")
        return False

    def generate_workshop_code(self, task_title, lang):
        """Taslağı Workshop klasörüne yazar"""
        file_name = self.clean_name(task_title)
        class_name = "".join(filter(str.isalnum, task_title.title())).replace(" ", "")
        if class_name[0].isdigit():
            class_name = "Dragon_" + class_name  # Örn: Dragon_2dEnvanterSistemi
        # ... (Template'ler aynı kalıyor) ...
        
        # DOSYA YOLU KONTROLÜ
        if template:
            # Workshop klasörünün tam yolundan emin olalım
            workshop_full_path = os.path.abspath(WORKSHOP_PATH)
            if not os.path.exists(workshop_full_path):
                os.makedirs(workshop_full_path)
                
            file_path = os.path.join(workshop_full_path, file_name + template["ext"])
            
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(template["code"])
                logger.info(f"🛠️ KOD DOSYASI OLUŞTU: {file_path}")
            except Exception as e:
                logger.error(f"❌ Kod yazılamadı: {e}")

        # Uygun şablonu bul
        template = templates.get(lang)
        if not template:
            # Eğer tam eşleşme yoksa (örn: sadece 'C#' yazıldıysa) esnek kontrol yap
            for key in templates:
                if key.split()[0] in lang:
                    template = templates[key]
                    break

        if template:
            file_path = os.path.join(WORKSHOP_PATH, file_name + template["ext"])
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(template["code"])
                logger.info(f"🛠️ Kod taslağı hazırlandı: {file_name}{template['ext']}")

    def scan_board_and_find_refs(self):
        """JSON dosyasını tara ve yeni görevler için işlemleri yap"""
        if not os.path.exists(BOARD_FILE):
            logger.error("❌ Board dosyası bulunamadı!")
            return False

        try:
            with open(BOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            success_count = 0
            for task in data.get("tasks", []):
                title = task.get("title")
                lang = task.get("language", "C# (Unity)")
                
                folder_name = self.clean_name(title)
                ref_folder = os.path.join(REF_PATH, folder_name)

                # Eğer bu görev için klasör yoksa, bu yenidir!
                if not os.path.exists(ref_folder):
                    logger.info(f"👁️ Yeni görev keşfedildi: {title}")
                    os.makedirs(ref_folder)
                    
                    # 1. Görsel Ganimet
                    self.download_preview(title, ref_folder)
                    
                    # 2. Kod Taslağı
                    self.generate_workshop_code(title, lang)
                    
                    # 3. Log Dosyası
                    with open(os.path.join(ref_folder, "research_note.txt"), "w", encoding="utf-8") as f:
                        f.write(f"🐉 DRAGON RESEARCH\nGörev: {title}\nDil: {lang}\nTarih: {datetime.now()}")
                    
                    success_count += 1

            if success_count > 0:
                logger.info(f"✅ Tarama bitti. {success_count} yeni ganimet toplandı.")
            return True

        except Exception as e:
            logger.error(f"❌ Scout Hatası: {e}")
            return False

if __name__ == "__main__":
    scout = DragonScout()
    scout.scan_board_and_find_refs()