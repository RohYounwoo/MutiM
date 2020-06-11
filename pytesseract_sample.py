import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import cv2
from googletrans import Translator
from googletrans import LANGUAGES
import numpy as np
from PIL import ImageFont, ImageDraw, Image



def readtext(src):
    img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(src)
    highHeight = 600
    lowHeight = 680
    img = img[highHeight:lowHeight, 350:900]

    #img = cv2.resize(img, (int(math.floor(1200/2)), int(math.floor((lowHeight - highHeight)/2))))
    #la_edge_img = cv2.Laplacian(img, -1)
    '''
    img_blurred = cv2.GaussianBlur(img, ksize=(5,5), sigmaX=0)
    img_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue = 255.0,
        adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )
    '''
    text = tess.image_to_string(img, lang="eng")
    if text:
        trans = Translator()
        t = trans.translate(
            text, src='en', dest='ko'
        )


        b,g,r,a = 255,255,255,0
        fontpath = "./fonts/gulim.ttc"
        font = ImageFont.truetype(fontpath, 60)
        img_pil = Image.fromarray(img2)
        draw = ImageDraw.Draw(img_pil)
        w, h = draw.textsize(text, font=font)
        draw.text(((img2.shape[1] - w)/2 ,30),  text, font=font, fill=(b,g,r,a))
        

        img2 = np.array(img_pil)

        #cv2.putText(img2, "absxsdga", (400,100), cv2.FONT_HERSHEY_DUPLEX, 3, (255,255,255))
        print(t.text)
    print(text)
    cv2.imshow("imgShow", img2)


readtext('./image/hosp.jpg')
