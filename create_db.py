from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the database URI components from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')

# Create a SQLAlchemy engine for creating the database
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}')

# Create the database if it doesn't exist
with engine.connect() as conn:
    try:
        conn.execute(text(f"CREATE DATABASE {db_name}"))
        print(f"Database '{db_name}' created successfully.")
    except ProgrammingError as e:
        if '1007 (HY000): Can\'t create database' in str(e):
            print(f"Database '{db_name}' already exists.")
        else:
            raise e

# Update the database URI to include the database name
database_uri = f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}'

app = Flask(__name__)

# Configure MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'Customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(255), nullable=False)

class Address(db.Model):
    __tablename__ = 'Addresses'
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'))

class Invoice(db.Model):
    __tablename__ = 'Invoices'
    invoice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_number = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_terms = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.customer_id'))

class InvoiceItem(db.Model):
    __tablename__ = 'Invoice_Items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('Invoices.invoice_id'))
    part_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    extended_amount = db.Column(db.Numeric(10, 2), nullable=False)

class FooterData(db.Model):
    __tablename__ = 'Footer_Data'
    footer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('Invoices.invoice_id'))
    additional_charges = db.Column(db.Numeric(10, 2))
    discount = db.Column(db.Numeric(10, 2))
    shipping_charges = db.Column(db.Numeric(10, 2))
    sub_total = db.Column(db.Numeric(10, 2))
    tax = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
