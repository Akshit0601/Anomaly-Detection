import tensorflow
import os
import numpy
import cv2

model = tensorflow.keras.models.load_model('/Users/akshitshishodia/intern/tracker/files/model_2.h5')
# path = '/Users/akshitshishodia/Desktop/Screen Recording 2023-07-07 at 10.20.02 PM.mov'
cap = cv2.VideoCapture('/Users/akshitshishodia/Desktop/Screen Recording 2023-07-07 at 10.20.02 PM.mov')

def convert_frame(frame):
    x = cv2.resize(frame,(512,512))
    x = (x-127.5)/127.5
    x = x.astype(numpy.float32)
    x = numpy.expand_dims(x,axis=0)
    return x


while(cap.isOpened()):
# for file in os.listdir(path=path):
    
    # frame = cv2.imread(os.path.join(path,file))

   


    ret,frame = cap.read()
    x = convert_frame(frame)
    prediction = model.predict(x)
    h = frame.shape[1]
    w = frame.shape[0]

    x1,y1,x2,y2 = prediction[0]

    x1 = int(x1*h)
    y1 = int(y1*w)

    x2 = int(x2*h)
    y2 = int(y2*w)
    frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),thickness=3)


    cv2.imshow('check',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()


