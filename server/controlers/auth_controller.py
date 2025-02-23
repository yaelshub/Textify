# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
import json

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