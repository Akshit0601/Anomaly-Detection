from segment_anything import SamPredictor,sam_model_registry
import tensorflow
import os
import logging
import cv2 as cv
import numpy as np
import pandas as pd


logging.basicConfig(filename='sim.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
csv_data = pd.DataFrame(columns=['x','y','name'])
BASE_PATH_1 = '/Users/akshitshishodia/tracker/roboDK /pred'
BASE_PATH_2 = '/Users/akshitshishodia/tracker/roboDK /test2'
model = tensorflow.keras.models.load_model('/Users/akshitshishodia/tracker/files/model_prev.h5')
sam  = sam = sam_model_registry["vit_b"](checkpoint="/Users/akshitshishodia/sam_vit_b_01ec64.pth")
sam.to(device='mps')
cnt = 0
def convert_frame(frame):

    x = cv.resize(frame,(512,512))
    x = (x-127.5)/127.5
    x = x.astype(np.float32) 
    x = np.expand_dims(x,axis=0)
    return x
def predict(path):
    global model,sam,cnt,csv_data,BASE_PATH_1
    data = cv.imread(path)    
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
    t = (x,y)
    t = str(t)
    logging.info(t)
    y1 = np.max(idx[0])
    x1 = np.max(idx[1])

    y2 = np.min(idx[0])
    x2 = np.min(idx[1])

    data = cv.rectangle(data,(x2,y1),(x1,y2),(0,255,0),5)
    data = cv.circle(data,(x,y),5,(0,255,0),-1)
    name = str(cnt)+'.png'
    cnt+=1
    path_save = os.path.join(BASE_PATH_1,name)
    cv.imwrite(path_save,data)
    
    csv_data = csv_data.append({'x':x,'y':y,'name':path},ignore_index=True)
    csv_data.to_csv('final_inventory_path_2.csv')



for file in os.listdir(BASE_PATH_2):
    predict(os.path.join(BASE_PATH_2,file))



        

        
        




