from robodk import robolink  # RoboDK API
from robodk import robomath  # Robot toolbox
import os

RDK = robolink.Robolink()


robolink.import_install('cv2', 'opencv-python', RDK)
robolink.import_install('numpy', RDK)
import numpy as np
import cv2 as cv

CAM_NAME = 'My Camera'
CAM_PARAMS = 'SIZE=640x480' 
WINDOW_NAME = 'My Camera Feed'
BASE_PATH = '/Users/akshitshishodia/tracker/DATASET_/DATASET_INV/NEW'
cnt = 459

cam_item = RDK.Item(CAM_NAME, robolink.ITEM_TYPE_CAMERA)
if not cam_item.Valid():
    cam_item = RDK.Cam2D_Add(RDK.AddFrame(CAM_NAME + ' Frame'), CAM_PARAMS)
    cam_item.setName(CAM_NAME)
cam_item.setParam('Open', 1)


while cam_item.setParam('isOpen') == '1' and cnt!= 600:

    img_socket = None
    bytes_img = RDK.Cam2D_Snapshot('', cam_item)
    if isinstance(bytes_img, bytes) and bytes_img != b'':
        nparr = np.frombuffer(bytes_img, np.uint8)
        img_socket = cv.imdecode(nparr, cv.IMREAD_COLOR)
    if img_socket is None:
        break

    if cnt%5 == 0 :
        name = 'frame'+str(cnt) + '.png'
        path  = os.path.join(BASE_PATH,name) 
        cv.imwrite(path,img_socket)
    cnt+=1
    key = cv.waitKey(1)
    if key == 27:
        break  
cv.destroyAllWindows()
RDK.Cam2D_Close(cam_item)