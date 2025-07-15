from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from server.services.file_analysis.extraction_and_cutting import extract_text_from_pdf
from server.services.model_training.bert.bert import analyze_text

text_bp = Blueprint('text', __name__)

# קולט קובץ, מחלץ את הטקסט מפעיל את המודל ומחזיר תשובה למשתמש
@text_bp.route("/collect_data", methods=["POST"])
def collect_data():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400
    #שומר את הקובץ שהגיע בבקשה- למשתנה 
    file = request.files['file']
    if file.filename == '':
        return {"error": "No file selected"}, 400
    
    try:
        #יוצר תיקייה בתוך התיקייה הראשית של הפרויקט.
        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        #ניקוי שם הקובץ מקודים זדוניים
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)

        text = extract_text_from_pdf(temp_path)
        # מחיקת הקובץ מהדיסק אחרי שחילץ המידע – כדי לא לבזבז מקום.
        os.remove(temp_path)
        #המודל מקבל את הטקסט ואת הנתיב למודל המאומן ומחזיר את שם המחבר שנחזה ואת מילון ההסתברויות לכל סופר
        predicted_label, prob_dict = analyze_text(text, "D:/Textify/server/services/model_training/BertModel")
        # float ממיר את כל הערכים במילון לערכים מסוג 
        prob_dict = {k: float(v) for k, v in prob_dict.items()}
    
        threshold = 0.85
        #מוצא את המחבר עם ההסתברות הכי גבוהה וההסתברות עצמה.
        top_author = max(prob_dict, key=prob_dict.get)
        top_prob = prob_dict[top_author]
        # אם ההסתברות הכי גבוהה נמוכה מהסף, מחזיר הודעה שהסופר אולי אינו קיים
        if top_prob < threshold:
            predicted_label = "The system is not sure enough about the author.\nThe text may have been written by an author who is not in the database."

        return jsonify({
            "label": predicted_label,
            "probabilities": prob_dict
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
