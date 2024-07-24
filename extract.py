import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import re

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.images = convert_from_path(pdf_path)
    
    def extract_text_from_region(self, x, y, w, h):
        extracted_texts = []
        for i, image in enumerate(self.images):
            image_np = np.array(image)
            roi = image_np[y:y+h, x:x+w]
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(gray_roi, config=custom_config)
            extracted_texts.append(text)
        return extracted_texts

    def process_top_left(self):
        texts_tl = self.extract_text_from_region(220, 10, 600, 200)
        results = []
        for text_tl in texts_tl:
            lines_tl = text_tl.splitlines()
            if len(lines_tl) >= 3:
                company_name = lines_tl[0]
                address_line1 = lines_tl[1]
                address_line2 = lines_tl[2]
            else:
                company_name = address_line1 = address_line2 = ""
            result = {
                "company_name": company_name,
                "address_line1": address_line1,
                "address_line2": address_line2
            }
            results.append(result)
        return results

    def process_top_right(self):
        texts_tr = self.extract_text_from_region(1300, 10, 600, 200)
        results = []
        for text_tr in texts_tr:
            lines_tr = text_tr.splitlines()

            if len(lines_tr) >= 4:
                invoice_number = lines_tr[0].rsplit(": ",1)[1]
                invoice_date = lines_tr[1].rsplit(": ",1)[1]
                due_date = lines_tr[3].rsplit(": ",1)[1]
                payment_terms = lines_tr[4].rsplit(": ",1)[1]
            else:
                invoice_number = invoice_date = due_date = payment_terms = ""
            result = {
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "due_date": due_date,
                "payment_terms": payment_terms
            }
            results.append(result)
        return results

    def process_billed_to(self):
        texts_bt = self.extract_text_from_region(50, 400, 750, 200)
        results = []
        for text_bt in texts_bt:
            lines_bt = text_bt.splitlines()
            if len(lines_bt) >= 3:
                company_name = lines_bt[0]
                address_line = lines_bt[1] + lines_bt[2]
            elif len(lines_bt) == 2:
                company_name = lines_bt[0]
                address_line = lines_bt[1]
            result = {
                "company_name": company_name,
                "address_line": address_line
            }
            results.append(result)
        return results

    def process_shipped_to(self):
        texts_bt = self.extract_text_from_region(800, 400, 800, 200)
        results = []
        for text_bt in texts_bt:
            lines_bt = text_bt.splitlines()
            if len(lines_bt) >= 3:
                company_name = lines_bt[0]
                address_line = lines_bt[1] + lines_bt[2]
            elif len(lines_bt) == 2:
                company_name = lines_bt[0]
                address_line = lines_bt[1]
            result = {
                "company_name": company_name,
                "address_line": address_line
            }
            results.append(result)
        return results

    def process_table_data(self):
        texts_part = self.extract_text_from_region(50, 750, 650, 600)
        results_part = []
        for text_part in texts_part:
            lines_part = text_part.splitlines()
            for line in lines_part:
                if line != '':
                    results_part.append(line)

        texts_quants = self.extract_text_from_region(700, 750, 200, 600)
        results_quant = []
        for text_quant in texts_quants:
            lines_quant = text_quant.splitlines()
            for line in lines_quant:
                if line != '':
                    results_quant.append(int(line))
        
        texts_prices = self.extract_text_from_region(1000, 750, 200, 600)
        results_price = []
        for text_price in texts_prices:
            lines_price = text_price.splitlines()
            for line in lines_price:
                if line != '':
                    line = line.replace(',','')
                    line = line.removeprefix('$')
                    results_price.append(float(line))

        texts_exts = self.extract_text_from_region(1400, 750, 200, 600)
        results_ext = []
        for text_ext in texts_exts:
            lines_ext = text_ext.splitlines()
            for line in lines_ext:
                if line != '':
                    line = line.replace(',','')
                    line = line.removeprefix('$')
                    results_ext.append(float(line))
        combined_data = []
        for part, quant, price, ext in zip(results_part, results_quant, results_price, results_ext):
            combined_data.append({
                'part_number': part,
                'quantity': quant,
                'price': price,
                'extended_amount': ext
            })
        return combined_data
    
    def process_footer_data(self):
        texts_footers = self.extract_text_from_region(1400, 1350, 200, 450)
        results_footer = []
        temp = []
        for text_footer in texts_footers:
            lines_part = text_footer.splitlines()
            for line in lines_part:
                if line != '':
                    temp.append(line)                

        sub_total = (float(temp[0].removeprefix('$').replace(',','')))
        shipping_charges = (float(temp[1].removeprefix('$').replace(',','')))
        additional_charges = (float(temp[2].removeprefix('$').replace(',','')))
        tax = (float(temp[3].removeprefix('$').replace(',','')))
        discount = (float(temp[4].removeprefix('($').replace(',','').replace(')','')))
        total = (float(temp[5].removeprefix('$').replace(',','')))

        results_footer.append({
            "sub_total": sub_total,
            "shipping_charges": shipping_charges,
            "additional_charges": additional_charges,
            "tax": tax,
            "discount": discount,
            "total": total
        })
        return results_footer

