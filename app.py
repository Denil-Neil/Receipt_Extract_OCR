from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from extract import PDFExtractor
from dotenv import load_dotenv
from datetime import datetime
from models import db, Customer, Address, Invoice, InvoiceItem, FooterData

# Load environment variables
load_dotenv()

# Update database URI to use mysql+mysqlconnector
database_uri = os.getenv('DB_URI')

app = Flask(__name__)

# Configure MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = './uploads'

# Initialize the database
db.init_app(app)

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
        footer_data = pdf_extractor.process_footer_data()
        
        # Insert data into the database
        customer = Customer(company_name=billed_to[0]['company_name'])
        db.session.add(customer)
        db.session.commit()
        
        address = Address(address=billed_to[0]['address_line'], customer_id=customer.customer_id)
        db.session.add(address)
        db.session.commit()
        
        invoice = Invoice(
            invoice_number=invoice_details[0]['invoice_number'],
            invoice_date=datetime.strptime(invoice_details[0]['invoice_date'], '%d-%m-%Y'),
            due_date=datetime.strptime(invoice_details[0]['due_date'], '%d-%m-%Y'),
            payment_terms=invoice_details[0]['payment_terms'],
            customer_id=customer.customer_id
        )
        db.session.add(invoice)
        db.session.commit()
        
        for item in table_data:
            invoice_item = InvoiceItem(
                invoice_id=invoice.invoice_id,
                part_number=item['part_number'],
                description=item.get('description', ''),
                quantity=item['quantity'],
                price=item['price'],
                extended_amount=item['extended_amount']
            )
            db.session.add(invoice_item)
        
        footer = FooterData(
            invoice_id=invoice.invoice_id,
            additional_charges=footer_data[0]['additional_charges'],
            discount=footer_data[0]['discount'],
            shipping_charges=footer_data[0]['shipping_charges'],
            sub_total=footer_data[0]['sub_total'],
            tax=footer_data[0]['tax'],
            total=footer_data[0]['total']
        )
        db.session.add(footer)
        db.session.commit()
        
        response = {
            "header": header,
            "invoice_details": invoice_details,
            "billed_to": billed_to,
            "shipped_to": shipped_to,
            "table_data": table_data,
            "footer_data": footer_data
        }
        return jsonify(response)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
