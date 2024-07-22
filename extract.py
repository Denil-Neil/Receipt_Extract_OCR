import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import numpy as np

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

    def draw_grid_lines(self, grid_size=50):
        for i, image in enumerate(self.images):
            image_np = np.array(image)
            height, width, _ = image_np.shape
            for y in range(0, height, grid_size):
                cv2.line(image_np, (0, y), (width, y), (0, 255, 0), 1)
            for x in range(0, width, grid_size):
                cv2.line(image_np, (x, 0), (x, height), (0, 255, 0), 1)
            cv2.imshow('Image with Grid Lines', image_np)

# pdf_extractor = PDFExtractor("./samples/1718343129462.pdf")
# # print(pdf_extractor.process_top_left())
# print(pdf_extractor.process_top_right())
# pdf_extractor.draw_grid_lines(grid_size=50)