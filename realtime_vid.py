import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import cv2
from googletrans import Translator
from googletrans import LANGUAGES
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import moviepy.editor as mp # 원본 영상에서 오디오 추출
import pygame # 영상 바로 출력을 위해


temptxt = ""

def readtext(img):
    global temptxt
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

    ret, img_thresh = cv2.threshold(img,200,255,cv2.THRESH_BINARY_INV)
    text = tess.image_to_string(img_thresh, lang="eng")
    print(text)
    if text:
        trans = Translator()
        t = trans.translate(
            text, src='en', dest='ko'
        )
        temptxt = t.text
        print(t.text)

    
video = "./image/HospitalPlaylist.mp4"


clip = mp.VideoFileClip(video)
clip.audio.write_audiofile("./image/extract_ver2.mp3") # 음원추출. 영상당 최초 1번만 할 것



cap = cv2.VideoCapture(video)
if cap.isOpened():
   # font for korean
   b,g,r,a = 255,255,255,0
   fontpath = "./fonts/gulim.ttc"
   font = ImageFont.truetype(fontpath, 60)
   
   fps = cap.get(cv2.CAP_PROP_FPS)
   delay = int(1000/fps)
   print('FPS: %f, Delay: %dms'%(fps, delay))
   count = 0

   width = int(cap.get(3)) # 가로 길이 가져오기
   height = int(cap.get(4)) # 세로 길이 가져오기 
   fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X') #DIVX 코덱 적용
   out = cv2.VideoWriter('./image/saved_video_ver2.mp4', fcc, fps, (width, height))

   while True:
        ret, frame = cap.read()
        if ret:
            
            if temptxt:
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                #w, h = draw.textsize(temptxt, font=font) # frame[1] - w
                draw.text((100, 30), temptxt, font=font, fill=(b,g,r,a))
                frame = np.array(img_pil)

            count += 1
            if count%20 == 0: # every 20 frame
               temptxt = "" # reset subtitle
               count = 0
               readtext(frame)
            #cv2.imshow("Video Player", frame)
            out.write(frame) # 영상 저장
            key = cv2.waitKey(delay) & 0xFF

            if key == ord('q') or key == 27:
                break
        else:
            break
else:
    print("Can't open video.")
    
cap.release()
out.release()

print("creating vid complete")
my_clip = mp.VideoFileClip('./image/saved_video_ver2.mp4') # 새 영상 
audio_background = mp.AudioFileClip('./image/extract_ver2.mp3') # 추출한 음원
final_clip = my_clip.set_audio(audio_background)

final_clip.preview()

cv2.waitKey(0)
cv2.destroyAllWindows()
