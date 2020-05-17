import cv2

video = "./image/sampleEngSUB.mp4"

cap = cv2.VideoCapture(video)
if cap.isOpened():
   fps = cap.get(cv2.CAP_PROP_FPS)
   delay = int(1000/fps)
   print('FPS: %f, Delay: %dms'%(fps, delay))
   while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Video Player", frame)
            key = cv2.waitKey(delay) & 0xFF

            if key == ord('q') or key == 27:
                break
        else:
            break
else:
    print("Can't open video.")
    
cap.release()
cv2.destroyAllWindows()
