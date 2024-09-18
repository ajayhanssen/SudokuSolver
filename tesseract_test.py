import cv2
import pytesseract
import numpy as np

image = cv2.imread('cells/cell_4_8.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# recognize number
number = pytesseract.image_to_string(gray, config='--psm 10 digits')

print(number)