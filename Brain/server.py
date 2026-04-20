from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD_FILE = os.path.join(BASE_DIR, "Archive", "dragon_board.json")

@app.route('/send-order', methods=['POST'])
def receive_order():
    try:
        new_task = request.json
        print(f"📩 Emir Geldi: {new_task['title']}")
        
        with open(BOARD_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data["tasks"].append(new_task)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"❌ Server Hatası: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)