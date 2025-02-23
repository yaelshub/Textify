# controllers/pdf_controller.py
from flask import Blueprint, request, jsonify
import PyPDF2

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/upload_pdf', methods=['POST'])
def upload_pdf():
	if 'file' not in request.files:
		return jsonify({"error": "No file part"}), 400

	file = request.files['file']
	if file.filename == '':
		return jsonify({"error": "No selected file"}), 400

	if file and file.filename.endswith('.pdf'):
		pdf_reader = PyPDF2.PdfFileReader(file)
		text = ""
		for page_num in range(pdf_reader.numPages):
			text += pdf_reader.getPage(page_num).extract_text()

		return jsonify({"text": text}), 200
	else:
		return jsonify({"error": "Invalid file type"}), 400