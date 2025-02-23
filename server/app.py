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
import json
import os

app = Flask(__name__)
USERS_FILE = "users.json"

# יצירת קובץ users.json אם אינו קיים
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as file:
        json.dump([], file)

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    if not all(key in data for key in ("fullName", "password", "phone", "email")):
        return jsonify({"error": "נתונים חסרים"}), 400

    # קריאת הנתונים הקיימים
    with open(USERS_FILE, "r") as file:
        users = json.load(file)

    # הוספת משתמש חדש
    users.append(data)

    # שמירת הנתונים חזרה לקובץ
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

    return jsonify({"message": "המשתמש נוסף בהצלחה!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
