import json
import shutil
import os

# KLASÖR YOLLARINI TANIMLIYORUZ (Senin istediğin gibi)
BRAIN_PATH = "./DragonBrain/"
ARCHIVE_PATH = "./DragonArchive/"

class DragonArchitect:
    def __init__(self, project_name):
        self.project_name = project_name
        self.board_filename = "dragon_board.json"
        self.data = {"project": project_name, "tasks": []}

    def create_task(self, title, lang, desc):
        task = {
            "title": title,
            "language": lang,
            "description": desc,
            "status": "todo"
        }
        self.data["tasks"].append(task)
        self.sync_to_github()

    def sync_to_github(self):
        # 1. Önce dosyayı yerelde oluştur
        with open(self.board_filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        
        # 2. Dosyayı DragonArchive klasörüne kopyala
        shutil.copy(self.board_filename, os.path.join(ARCHIVE_PATH, self.board_filename))
        print(f"✅ {self.board_filename} arşive kopyalandı.")

# Başlat
architect = DragonArchitect("Dragon's Escape")
architect.create_task("Karakter Kontrolcü", "C#", "Zıplama ve yürüme logları dahil")