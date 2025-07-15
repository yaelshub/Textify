from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os
from server.controllers.auth_controller import auth_bp
from server.controllers.text_controller import text_bp
import os
import runpy
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
base_path = os.path.dirname(os.path.abspath(__file__))  
target_script = os.path.join(base_path, "services", "file_analysis", "feature_extraction.py")
# runpy.run_path(target_script)

USERS_FILE = "users.json"

# יצירת קובץ users.json אם אינו קיים
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as file:
        json.dump([], file)
else:
    with open(USERS_FILE, "r") as file:
        try:
            json.load(file)
        except json.JSONDecodeError:
            with open(USERS_FILE, "w") as file:
                json.dump([], file)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(text_bp, url_prefix='/text')



if __name__ == "__main__":
    app.run(debug=True ,host='127.0.0.1', port=5000)
