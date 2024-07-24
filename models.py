
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
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