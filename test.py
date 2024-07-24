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

footer = pdf_extractor.process_footer_data()

print(footer)