import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import cv2

img = cv2.imread('./image/anything.jpg')
text = tess.image_to_string(img)


print(text)
