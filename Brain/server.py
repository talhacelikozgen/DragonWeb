"""Dragon Server - Frontend ile iletişim"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD_FILE = os.path.join(BASE_DIR, "Archive", "dragon_board.json")
BOARD_LOCK = threading.Lock()  # Race condition önlemek için

def validate_task(task):
    """Görev verilerini doğrula"""
    if not isinstance(task, dict):
        return False, "Görev obje olmak zorunda"
    
    required_fields = ["title", "language", "description", "status"]
    for field in required_fields:
        if field not in task:
            return False, f"Eksik alan: {field}"
    
    if not isinstance(task["title"], str) or not task["title"].strip():
        return False, "Başlık boş olamaz ve string olmak zorunda"
    
    if not isinstance(task["language"], str) or task["language"] not in ["C# (Unity)", "Java (Sistem)", "Python (AI)"]:
        return False, f"Geçersiz dil: {task['language']}"
    
    if task["status"] not in ["todo", "in_progress", "done"]:
        return False, f"Geçersiz durum: {task['status']}"
    
    return True, "Validation geçti"

@app.route('/send-order', methods=['POST'])
def receive_order():
    """Yeni görev al ve kaydet"""
    try:
        new_task = request.json
        
        if not new_task:
            logger.warning("Boş görev yapısı geldi")
            return jsonify({"status": "error", "message": "Görev boş olamaz"}), 400
        
        # Validasyon
        valid, message = validate_task(new_task)
        if not valid:
            logger.warning(f"Geçersiz görev: {message} - {new_task}")
            return jsonify({"status": "error", "message": message}), 400
        
        logger.info(f"📩 Emir geldi: {new_task['title']}")
        
        # Race condition önlemek için lock
        with BOARD_LOCK:
            if not os.path.exists(BOARD_FILE):
                logger.error(f"Board dosyası bulunamadı: {BOARD_FILE}")
                return jsonify({"status": "error", "message": "Board dosyası bulunamadı"}), 500
            
            try:
                with open(BOARD_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                logger.error("Board JSON bozuk")
                return jsonify({"status": "error", "message": "Board dosyası bozuk"}), 500
            
            # Timestamp ekle
            new_task["created_at"] = datetime.now().isoformat()
            new_task["id"] = len(data.get("tasks", [])) + 1
            
            # Listeyi başlat
            if "tasks" not in data:
                data["tasks"] = []
            
            data["tasks"].append(new_task)
            
            try:
                with open(BOARD_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                logger.info(f"✅ Görev kaydedildi: {new_task['title']}")
            except IOError as e:
                logger.error(f"Dosya yazma hatası: {e}")
                return jsonify({"status": "error", "message": "Kayıt hatası"}), 500
        
        return jsonify({"status": "success", "task": new_task}), 200
    
    except Exception as e:
        logger.error(f"❌ Server kritik hatası: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Sunucu hatası"}), 500

@app.route('/get-board', methods=['GET'])
def get_board():
    """Tüm board verilerini getir"""
    try:
        if not os.path.exists(BOARD_FILE):
            return jsonify({"tasks": [], "logs": []}), 200
        
        with open(BOARD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Board getirme hatası: {e}")
        return jsonify({"status": "error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Sunucu sağlık kontrolü"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    logger.info("🐉 Dragon Server başlatıldı (http://0.0.0.0:5000)")
    app.run(host='0.0.0.0', port=5000, debug=False)