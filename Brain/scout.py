import json
import os
import requests
import logging
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
        for path in [REF_PATH, WORKSHOP_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info(f"Klasör oluşturuldu: {path}")

    def turkish_to_english(self, text):
        """Türkçe karakterleri İngilizce'ye dönüştür ve dosya adı formatına çevir"""
        if not text:
            return "unnamed"
        chars = {"ç": "c", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ı": "i", "İ": "I", "Ç": "C", "Ş": "S", "Ğ": "G", "Ü": "U", "Ö": "O"}
        for tr, en in chars.items():
            text = text.replace(tr, en)
        return text.replace(" ", "_").lower().strip()

    def download_preview(self, keyword, folder):
        """İnternetten görev için preview görsel indir"""
        img_url = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400"
        try:
            response = requests.get(img_url, timeout=5)
            if response.status_code == 200:
                preview_path = os.path.join(folder, "preview.jpg")
                with open(preview_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Preview indirildi: {preview_path}")
                return True
        except requests.RequestException as e:
            logger.warning(f"Preview indirme başarısız ({keyword}): {e}")
        except IOError as e:
            logger.error(f"Dosya yazma hatası: {e}")
        return False
    
    def generate_workshop_code(self, task_title, lang):
        """Dil bazlı kod taslağı oluştur"""
        file_name = self.turkish_to_english(task_title)
        class_name = task_title.replace(' ', '').replace('-', '')
        
        code_templates = {
            "C# (Unity)": {
                "ext": ".cs",
                "code": f"""using UnityEngine;

public class {class_name} : MonoBehaviour
{{
    void Start()
    {{
        Debug.Log(\"🐉 Dragon: {task_title} sistemi aktif.\");
    }}
}}"""
            },
            "Java (Sistem)": {
                "ext": ".java",
                "code": f"""public class {class_name} {{
    public static void main(String[] args) {{
        System.out.println(\"🐉 Dragon: {task_title} baslatildi.\");
    }}
}}"""
            },
            "Python (AI)": {
                "ext": ".py",
                "code": f"""# Dragon Task: {task_title}
# Oluşturulma tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

class {class_name}:
    def __init__(self):
        print(f\"🐉 Dragon: {task_title} başlatıldı.\")

if __name__ == \"__main__\":
    task = {class_name}()
"""
            }
        }
        
        # Dil desteğini kontrol et
        template = None
        for key, value in code_templates.items():
            if key in lang or lang in key:
                template = value
                break
        
        if not template:
            logger.warning(f"Desteklenmeyen dil: {lang}. Ayarlar: {', '.join(code_templates.keys())}")
            return
        
        file_path = os.path.join(WORKSHOP_PATH, file_name + template["ext"])
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(template["code"])
                logger.info(f"Kod taslağı oluşturuldu: {file_path}")
            except IOError as e:
                logger.error(f"Kod taslağı yazma hatası: {e}")

    def scan_board_and_find_refs(self):
        """Board'daki görevleri tara ve referansları oluştur"""
        if not os.path.exists(BOARD_FILE):
            logger.error(f"Board dosyası bulunamadı: {BOARD_FILE}")
            return False

        try:
            with open(BOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Board JSON hatası: {e}")
            return False
        except IOError as e:
            logger.error(f"Board okuma hatası: {e}")
            return False
        
        if "tasks" not in data or not isinstance(data["tasks"], list):
            logger.warning("Board'da 'tasks' anahtarı veya format yok")
            return False
        
        success_count = 0
        for task in data["tasks"]:
            try:
                if not isinstance(task, dict) or "title" not in task:
                    logger.warning(f"Geçersiz görev formatı: {task}")
                    continue
                    
                keyword = task["title"]
                lang = task.get("language", "Unknown")
                clean_folder_name = self.turkish_to_english(keyword)
                ref_folder = os.path.join(REF_PATH, clean_folder_name)
                
                if not os.path.exists(ref_folder):
                    os.makedirs(ref_folder)
                    logger.info(f"👁️ Scout: '{keyword}' için klasör oluşturuldu")
                    
                    # Git takibi için .gitkeep
                    gitkeep_path = os.path.join(ref_folder, ".gitkeep")
                    with open(gitkeep_path, "w") as f:
                        f.write("")
                    
                    # Referans Logu
                    log_path = os.path.join(ref_folder, "ref_log.txt")
                    with open(log_path, "w", encoding='utf-8') as log:
                        log.write(f"Görev: {keyword}\n")
                        log.write(f"Dil: {lang}\n")
                        log.write(f"Oluşturulma: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        log.write(f"Dragon Scout tarafından otomatik oluşturuldu.\n")
                    
                    # Kod taslağı
                    self.generate_workshop_code(keyword, lang)
                    
                    # Görsel Ganimet
                    self.download_preview(keyword, ref_folder)
                    success_count += 1
            except Exception as e:
                logger.error(f"Görev işleme hatası '{keyword}': {e}")
                continue
        
        logger.info(f"✅ Scout taraması tamamlandı. {success_count} yeni görev işlendi.")
        return True

if __name__ == "__main__":
    try:
        scout = DragonScout()
        scout.scan_board_and_find_refs()
    except Exception as e:
        logger.critical(f"Scout kritik hatası: {e}", exc_info=True)