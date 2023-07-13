import cv2
import numpy as np
import os
import time
import pandas 

frameSize = (500, 500)
cnt = 0
out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
data = pandas.DataFrame(columns=[time,'x','y'])

while(1):
    if cnt == 324:
        break
    name = 'frAme'+str(cnt)+'.jpg'
    img = cv2.imread(os.path.join('/Users/akshitshishodia/tracker/out_b',name))
    cnt+=1

    cv2.imshow('check',img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
cv2.destroyAllWindows()
out.release()