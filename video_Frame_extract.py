import cv2
import os


cap = cv2.VideoCapture('/Users/akshitshishodia/Desktop/Screen Recording 2023-07-07 at 3.39.48 PM.mov')
cnt = 0

while cap.isOpened():
    ret,frame = cap.read()
    if cnt%2 == 0:
        filename = 'frame' + str(cnt)+'.png'
        ouputPath = os.path.join('/Users/akshitshishodia/intern/tracker/DATASET_',filename)
        cv2.imwrite(ouputPath,frame)
    cnt+=1

cap.release()
