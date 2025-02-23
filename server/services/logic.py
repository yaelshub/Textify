class BusinessLogic:
    def process_data(self, data):
        return f"Processed data: {data}"
    from flask import Flask, request, jsonify

# יצירת אובייקט Flask
app = Flask(__name__)

# יצירת מחלקת BusinessLogic
class BusinessLogic:
    def process_data(self, data):
        return f"Processed data: {data}"

# יצירת אובייקט של BusinessLogic
business_logic = BusinessLogic()

# מסלול לביצוע פעולה עם BusinessLogic
@app.route('/process', methods=['POST'])
def process_data():
    data = request.json.get("data")  # מקבלים את המידע מה-POST
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # שימוש ב-BusinessLogic לעיבוד הנתונים
    processed_data = business_logic.process_data(data)
    
    # מחזירים את התוצאה ללקוח
    return jsonify({"processed_data": processed_data})

if __name__ == '__main__':
    app.run(debug=True)
