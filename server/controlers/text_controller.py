from flask import Blueprint, request, jsonify
import io
from server.services.File_analysis.file_analysis import main
from server.services.File_analysis.extraction_and_cutting import extract_text_from_pdf
text_bp = Blueprint('text', __name__)



@text_bp.route("/collect_data", methods=["POST"])
def collect_data():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        file_stream = io.BytesIO(file.read())
        text = extract_text_from_pdf(file_stream)

        # הרצת הפונקציה
        results = main(text)

        # הדפסת תוצאות בצד השרת
        print("=== תוצאות ניתוח הטקסט ===")
        for key, value in results.items():
            if isinstance(value, str) and value.startswith("שגיאה:"):
                print(f"בעיה ב-{key}: {value}")
            else:
                print(f"{key} - עבד בהצלחה")
        print("===========================")

        return jsonify({"message": "Data collected successfully", "data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500