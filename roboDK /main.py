from multiprocessing import Queue

from multiprocessing import Process
import predict
from robodk import robolink 
from robodk import robomath 
import numpy as np
import cv2 as cv

RDK = robolink.Robolink()
CAM_NAME = 'My Camera'
CAM_PARAMS = 'SIZE=640x480'
WINDOW_NAME = 'My Camera Feed'
queue = Queue()
task = Process(target=predict.predict,args=(queue,))
task.start()


cam_item = RDK.Item(CAM_NAME, robolink.ITEM_TYPE_CAMERA)
if not cam_item.Valid():
    cam_item = RDK.Cam2D_Add(RDK.AddFrame(CAM_NAME + ' Frame'), CAM_PARAMS)
    cam_item.setName(CAM_NAME)
cam_item.setParam('Open', 1)

while cam_item.setParam('isOpen') == '1':

    img_socket = None
    bytes_img = RDK.Cam2D_Snapshot('', cam_item)
    if isinstance(bytes_img, bytes) and bytes_img != b'':
        nparr = np.frombuffer(bytes_img, np.uint8)
        img_socket = cv.imdecode(nparr, cv.IMREAD_COLOR)
    if img_socket is None:
        break
    
    queue.put(img_socket)
    cv.imshow(WINDOW_NAME, img_socket)
    key = cv.waitKey(1)
    if key == 27:
        queue.put(None)
        break  
queue.put(None)
cv.destroyAllWindows()
RDK.Cam2D_Close(cam_item)
