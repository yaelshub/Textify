# f2get("name", "אורח")  # ברירת מחדל אם לא נשלח שם
#     response = {"message": f"ברוכים הבאים {name}!"}
#     return jsonify(response)  # החזרת תשובה בפורמט JSON

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)  # הפעלת השרת
# from flask import Flask, request, jsonify
# app = Flask(__name__)
# @app.route('/welcome', methods=['POST'])
# def welcome():
#     data = request.get_json()
#     name = data.get("name", "אורח")  # ברירת מחדל אם לא נשלח שם
#     return jsonify({"message": f"ברוכים הבאים {name}!"})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # מתיר ל-React לגשת לשרת

# users = []  # רשימה לשמירת המשתמשים

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     data = request.get_json()
#     name = data.get("name")
    
#     if not name:
#         return jsonify({"error": "יש לספק שם"}), 400

#     users.append(name)
#     return jsonify({"message": f"משתמש {name} נוסף בהצלחה!"})

# @app.route('/get_users', methods=['GET'])
# def get_users():
#     return jsonify({"users": users})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask
import json
import os
# import sys
from controlers.auth_controller import auth_bp
from controlers.pdf_controller import pdf_bp
from controlers.text_analysis_controller import text_analysis_bp
import io
from services.File_analysis.extract_from_PDF import extract_text_from_pdf
from services.File_analysis.collect_data import calculate_average_word_count
from services.File_analysis.tokenization import tokenize_text

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

@app.route("/extract_text", methods=["POST"])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # בדיקה אם נבחר קובץ
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # עיבוד הקובץ ישירות בזיכרון
    try:
        file_stream = io.BytesIO(file.read())  # יצירת זרם של הקובץ
        #todo: remember to check what the result of the function is
        text = extract_text_from_pdf(file_stream)  # קריאה לפונקציה לעיבוד קובץ PDF
        tokens = tokenize_text(text)
        sents= tokens["sent"]
        words=tokens["words"]
        collect_data=calculate_average_word_count(text)
        return jsonify({"text": text, "sentences": sents, "words": words, "info": collect_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(pdf_bp, url_prefix='/pdf')
app.register_blueprint(text_analysis_bp, url_prefix='/text_analysis')

if __name__ == "__main__":
    app.run(debug=True ,host='127.0.0.1', port=5000)








 