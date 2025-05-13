from flask import Blueprint, request, jsonify
from services.File_analysis.main import main
text_bp = Blueprint('text', __name__)


@text_bp.route("/collect_data", methods=["POST"])
def collect_data():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    try:
        response = main(file)
        return jsonify({"message": "Data collected successfully", "data": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
