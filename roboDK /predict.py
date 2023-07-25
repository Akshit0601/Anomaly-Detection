from segment_anything import SamPredictor,sam_model_registry
import tensorflow
import os
from multiprocessing import Queue
import logging
import cv2 as cv
import numpy as np

logging.basicConfig(filename='sim.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)

model = tensorflow.keras.models.load_model('/Users/akshitshishodia/tracker/files/model_prev.h5')
sam  = sam = sam_model_registry["vit_b"](checkpoint="/Users/akshitshishodia/sam_vit_b_01ec64.pth")
sam.to(device='mps')

def convert_frame(frame):
    x = cv.resize(frame,(512,512))
    x = (x-127.5)/127.5
    x = x.astype(np.float32) 
    x = np.expand_dims(x,axis=0)
    return x
def predict(queue:Queue):
    global model,sam
    while(1):
        data = queue.get()
        if data is None:
            break
        h = data.shape[1]
        w = data.shape[0]
        x = convert_frame(data)
        prediction = model.predict(x)
        x1,y1,x2,y2 = prediction[0]
        x1 = int(x1*h)
        y1 = int(y1*w)
        x2 = int(x2*h)
        y2 = int(y2*w)
        input_box = np.array([x1,y1,x2,y2])
        predictor = SamPredictor(sam)
        clone = cv.cvtColor(data,cv.COLOR_BGR2RGB)
        predictor.set_image(clone)
        masks,_,_ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_box[None,:],
            multimask_output=False,
        )
        idx = np.where(masks[0] == True)
        y = int(idx[0].mean())
        x = int(idx[1].mean())
        logging.info(x)
        logging.info(y)

        

        
        




