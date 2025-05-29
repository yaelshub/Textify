from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask
import json, os
from controlers.auth_controller import auth_bp
from controlers.text_controller import text_bp
import os
import runpy

base_path = os.path.dirname(os.path.abspath(__file__))  # זה יביא את הנתיב ל-app.py
target_script = os.path.join(base_path, "services", "file_analysis", "feature_extraction.py")
runpy.run_path(target_script)
app = Flask(__name__)
CORS(app)  
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

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    if not all(key in data for key in ("fullName", "email")):
        return jsonify({"error": "Missing data"}), 400

    # קריאת הנתונים הקיימים
    with open(USERS_FILE, "r") as file:
        users = json.load(file)

    # הוספת משתמש חדש
    users.append(data)

    # שמירת הנתונים חזרה לקובץ
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

    return jsonify({"message": "User added successfully!"}), 201

@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    if not all(key in data for key in ("fullName", "email")):
        return jsonify({"error": "missing data"}), 400

    # קריאת הנתונים הקיימים
    with open(USERS_FILE, "r") as file:
        users = json.load(file)

    # check if user exists
    for user in users:
        if user.get("fullName") == data["fullName"] and user.get("email") == data["email"]:
            return jsonify({"message": "User found"}), 200

    return jsonify({"error": "user not found"}), 404

@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    name = data.get("name")

    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            users = json.load(f)

        users = [user for user in users if user["name"] != name]

        with open(users_file, "w") as f:
            json.dump(users, f, indent=2)

    return jsonify({"message": f"{name} removed"}), 200



app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(text_bp, url_prefix='/text')



if __name__ == "__main__":
    app.run(debug=True ,host='127.0.0.1', port=5000)
