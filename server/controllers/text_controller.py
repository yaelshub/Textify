from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from server.services.file_analysis.extraction_and_cutting import extract_text_from_pdf
from server.services.model_training.bert.bert import analyze_text

text_bp = Blueprint('text', __name__)

@text_bp.route("/collect_data", methods=["POST"])
def collect_data():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"error": "No file selected"}, 400
    
    try:
        filename = secure_filename(file.filename)
        temp_path = os.path.join("/tmp", filename)  
        
        file.save(temp_path)  # שמירה פיזית של הקובץ

        # עכשיו אפשר לשלוח את הנתיב לפונקציה שלך
        text = extract_text_from_pdf(temp_path)
        os.remove(temp_path)
        predicted_label, prob_dict = analyze_text(text, "D:/Textify/server/services/model_training/BertModel")

        return jsonify({
            "label": predicted_label,
            "probabilities": prob_dict
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500