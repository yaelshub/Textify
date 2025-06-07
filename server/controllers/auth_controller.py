# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
import json
import os

auth_bp = Blueprint('auth', __name__)

USERS_FILE = 'users.json'

@auth_bp.route('/register', methods=['POST'])
def register():
	data = request.json
	if not all(key in data for key in ("fullName", "password", "phone", "email")):
		return jsonify({"error": "נתונים חסרים"}), 400

	with open(USERS_FILE, "r") as file:
		users = json.load(file)
	users.append(data)
	with open(USERS_FILE, "w") as file:
		json.dump(users, file, indent=4)

	return jsonify({"message": "המשתמש נוסף בהצלחה!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
	data = request.json
	email = data.get("email")
	password = data.get("password")

	with open(USERS_FILE, "r") as file:
		users = json.load(file)

	user = next((u for u in users if u["email"] == email and u["password"] == password), None)
	if user:
		return jsonify({"message": "התחברות הצליחה"}), 200
	else:
		return jsonify({"error": "אימייל או סיסמה שגויים"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "אימייל לא סופק"}), 400

    if not os.path.exists(USERS_FILE):
        return jsonify({"error": "קובץ משתמשים לא נמצא"}), 500

    with open(USERS_FILE, "r") as file:
        users = json.load(file)

    # מסנן את המשתמשים כדי להשאיר רק את אלו שלא שייכים לאימייל הזה
    filtered_users = [user for user in users if user["email"] != email]

    with open(USERS_FILE, "w") as file:
        json.dump(filtered_users, file, indent=4)

    return jsonify({"message": f"המשתמש {email} הוסר בהצלחה"}), 200