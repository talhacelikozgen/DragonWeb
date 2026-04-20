from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app) # Siteden gelen isteklere izin ver

# Yollar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD_FILE = os.path.join(BASE_DIR, "Archive", "dragon_board.json")

@app.route('/send-order', methods=['POST'])
def receive_order():
    new_task = request.json
    
    # Mevcut veriyi oku
    with open(BOARD_FILE, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data["tasks"].append(new_task)
        # Dosyanın başına dön ve üzerine yaz
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()
    
    print(f"🐉 Dragon Brain: Yeni emir alındı ve Arşive işlendi: {new_task['title']}")
    return jsonify({"status": "success", "message": "Emir Arşive İşlendi"})

if __name__ == '__main__':
    app.run(port=5000) # Bilgisayarında 5000 portunda çalışır