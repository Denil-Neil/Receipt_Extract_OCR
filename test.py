import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import numpy as np
from extract import PDFExtractor

# Path to the PDF file
pdf_path = "./samples/1718343157880.pdf"

# Convert PDF to a list of PIL images
images = convert_from_path(pdf_path)

pdf_extractor = PDFExtractor(pdf_path)

# print(pdf_extractor.process_billed_to())
top_left = pdf_extractor.process_top_left()
top_right = pdf_extractor.process_top_right()
billed_to = pdf_extractor.process_billed_to()
shipped_to = pdf_extractor.process_shipped_to()
table_data = pdf_extractor.process_table_data()

print(top_left, '\n', top_right, '\n',billed_to, '\n',shipped_to, '\n',table_data)