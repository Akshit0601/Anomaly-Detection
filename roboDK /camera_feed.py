
from robodk import robolink  # RoboDK API
from robodk import robomath  # Robot toolbox
RDK = robolink.Robolink()
import numpy as np
import cv2 as cv
CAM_NAME = 'Camera 1'
CAM_PARAMS = 'SIZE=640x480' 
WINDOW_NAME = 'My Camera Feed'
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
    img_png = None
    import tempfile
    with tempfile.TemporaryDirectory(prefix='robodk_') as td:
        tf = td + '/temp.png'
        if RDK.Cam2D_Snapshot(tf, cam_item) == 1:
            img_png = cv.imread(tf)
    if img_png is None:
        break
    cv.imshow(WINDOW_NAME, img_socket)
    key = cv.waitKey(1)
    if key == 27:
        break 
    if cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE) < 1:
        break 
cv.destroyAllWindows()
RDK.Cam2D_Close(cam_item)