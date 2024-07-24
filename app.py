from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from extract import PDFExtractor
from dotenv import load_dotenv

load_dotenv()

database_uri = os.getenv('DB_URI')

app = Flask(__name__)

## Add MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route("/")
def upload_form():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        pdf_extractor = PDFExtractor(filepath)
        header = pdf_extractor.process_top_left()
        invoice_details = pdf_extractor.process_top_right()
        billed_to = pdf_extractor.process_billed_to()
        shipped_to = pdf_extractor.process_shipped_to()
        table_data = pdf_extractor.process_table_data()
        response = {
            "header": header,
            "invoice_details": invoice_details,
            "billed_to": billed_to,
            "shipped_to": shipped_to,
            "table_data": table_data,
        }
        return jsonify(response)
@app.route("/test")
def test():
    return "Flask is running!", 200

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
