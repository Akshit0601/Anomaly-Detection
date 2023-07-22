
from robodk import robolink  # RoboDK API
from robodk import robomath  # Robot toolbox
RDK = robolink.Robolink()
import numpy as np
import cv2 as cv
import os
from segment_anything import SamPredictor,sam_model_registry
import pandas
import tensorflow
from time import time

cnt = 0
sam = sam_model_registry["vit_b"](checkpoint="/Users/akshitshishodia/sam_vit_b_01ec64.pth")
sam.to(device='mps')
data = pandas.DataFrame(columns=['time','x','y'])
model = tensorflow.keras.models.load_model('/Users/akshitshishodia/tracker/files/model_prev.h5')

def convert_frame(frame):
    x = cv.resize(frame,(512,512))
    x = (x-127.5)/127.5
    x = x.astype(np.float32) 
    x = np.expand_dims(x,axis=0)
    return x


CAM_NAME = 'My Camera'
CAM_PARAMS = 'SIZE=640x480' 
WINDOW_NAME = 'My Camera Feed'
cam_item = RDK.Item(CAM_NAME, robolink.ITEM_TYPE_CAMERA)
if not cam_item.Valid():
    cam_item = RDK.Cam2D_Add(RDK.AddFrame(CAM_NAME + ' Frame'), CAM_PARAMS)
    cam_item.setName(CAM_NAME)
cam_item.setParam('Open', 1)
t_no = time()



while cam_item.setParam('isOpen') == '1':


    img_socket = None
    bytes_img = RDK.Cam2D_Snapshot('', cam_item)
    if isinstance(bytes_img, bytes) and bytes_img != b'':
        nparr = np.frombuffer(bytes_img, np.uint8)
        img_socket = cv.imdecode(nparr, cv.IMREAD_COLOR)
    if img_socket is None:
        break
    img_png = None
    import tempfile
    with tempfile.TemporaryDirectory(prefix='robodk_') as td:
        tf = td + '/temp.png'
        if RDK.Cam2D_Snapshot(tf, cam_item) == 1:
            img_png = cv.imread(tf)
    if img_png is None:
        break

    h = img_socket.shape[1]
    w = img_socket.shape[0]
    # print(img_socket.shape)
    
    x = convert_frame(img_socket) 
  


    prediction = model.predict(x)
    x1,y1,x2,y2 = prediction[0]

    predictor = SamPredictor(sam)
    clone = cv.cvtColor(img_socket,cv.COLOR_BGR2RGB)
    print(img_socket.shape)
    predictor.set_image(clone)

    x1 = int(x1*h)
    y1 = int(y1*w)

    x2 = int(x2*h)
    y2 = int(y2*w)

    input_box = np.array([x1,y1,x2,y2])
    masks,_,_ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None,:],
        multimask_output=False,
    )
    idx = np.where(masks[0] == True)
    y = int(idx[0].mean())
    x = int(idx[1].mean())
    print(x,y)
    t = time()-t_no
    data = data.append({'time':t,'x':x,'y':y},ignore_index=True)
    data.to_csv("inventory_path.csv")

    y1 = np.max(idx[0])
    x1 = np.max(idx[1])

    y2 = np.min(idx[0])
    x2 = np.min(idx[1])

    img_socket = cv.rectangle(img_socket,(x2,y1),(x1,y2),(0,255,0),5)
    img_socket = cv.circle(img_socket,(x,y),5,(0,255,0),-1)

    name = 'out'+str(cnt)+'.jpg'
    path = os.path.join('/Users/akshitshishodia/tracker/inventoru out',name)
    cv.imwrite(path,img_socket)
    cnt+=1



 
  
    # img_socket = cv.rectangle(img_socket,(x1,y1),(x2,y2),(0,255,0),thickness=3)
    # if cnt%2 == 0 :
    #     name = str(cnt) + '.png'
    #     path  = os.path.join(base_path,name) 
    #     cv.imwrite(path,img_socket)
    # cnt+=1
    # cv.imshow('detect',img_socket)
    # key = cv.waitKey(1)
    # if key == 27:
    #     break 
    # if cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE) < 1:
    #     break 
cv.destroyAllWindows()
RDK.Cam2D_Close(cam_item)