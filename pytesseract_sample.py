import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import cv2


def readtext(src):
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    HalfHeight = int(len(img[:,1])/2)
    img = img[HalfHeight:, :]

    #la_edge_img = cv2.Laplacian(img, -1)
    
    text = tess.image_to_string(img)
    print(text)


readtext('./image/anything.jpg')
