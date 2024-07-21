import cv2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import numpy as np

# Path to the PDF file
pdf_path = "./samples/1718343129462.pdf"

# Convert PDF to a list of PIL images
images = convert_from_path(pdf_path)

# Iterate over each image
for i, image in enumerate(images):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Get image dimensions
    height, width, _ = image_np.shape

    # Draw horizontal lines
    for y in range(0, height, 50):
        cv2.line(image_np, (0, y), (width, y), (0, 255, 0), 1)

    # Draw vertical lines
    for x in range(0, width, 50):
        cv2.line(image_np, (x, 0), (x, height), (0, 255, 0), 1)

    # Display the image with grid lines
    cv2.imshow('Image with Grid Lines', image_np)
    cv2.waitKey(0)

cv2.destroyAllWindows()
