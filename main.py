import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import numpy as np

# Path to the PDF file
pdf_path = "./samples/1718343129462.pdf"

# Convert PDF to a list of PIL images
images = convert_from_path(pdf_path)

# Extract text from the top left region
for i, image in enumerate(images):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Define the region of interest (ROI) for the top left area
    x, y, w, h = 220, 10, 600, 200  # Example coordinates
    roi_tl = image_np[y:y+h, x:x+w]

    # Convert the ROI to grayscale
    gray_roi_tl = cv2.cvtColor(roi_tl, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to extract text from the ROI
    custom_config = r'--oem 3 --psm 6'
    text_tl = pytesseract.image_to_string(gray_roi_tl, config=custom_config)

    print("Extracted Text from Top Left Region:")
    print(text_tl)

    # Split the text into lines
    lines_tl = text_tl.splitlines()

    # Assign each line to a variable
    if len(lines_tl) >= 3:
        company_name = lines_tl[0]
        address_line1 = lines_tl[1]
        address_line2 = lines_tl[2]
    else:
        company_name = address_line1 = address_line2 = ""

    print("Company Name:", company_name)
    print("Address Line 1:", address_line1)
    print("Address Line 2:", address_line2)

# Extract text from the top right region
for i, image in enumerate(images):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Define the region of interest (ROI) for the top right area
    x, y, w, h = 1300, 10, 600, 200  # Example coordinates
    roi_tr = image_np[y:y+h, x:x+w]

    # Convert the ROI to grayscale
    gray_roi_tr = cv2.cvtColor(roi_tr, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to extract text from the ROI
    custom_config = r'--oem 3 --psm 6'
    text_tr = pytesseract.image_to_string(gray_roi_tr, config=custom_config)

    print("Extracted Text from Top Right Region:")
    print(text_tr)

    # Split the text into lines
    lines_tr = text_tr.splitlines()

    # Assign each line to a variable
    if len(lines_tr) >= 4:
        invoice_number = lines_tr[0]
        invoice_date = lines_tr[1]
        due_date = lines_tr[2]
        payment_terms = lines_tr[3]
    else:
        invoice_number = invoice_date = due_date = payment_terms = ""

    print("Invoice Number:", invoice_number)
    print("Invoice Date:", invoice_date)
    print("Due Date:", due_date)
    print("Payment Terms:", payment_terms)

    # Display the ROI (optional)
    cv2.imshow('ROI', roi_tr)
    cv2.waitKey(0)

cv2.destroyAllWindows()
