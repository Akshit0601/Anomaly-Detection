
from robodk import robolink 
from robodk import robomath 
import numpy as np
import cv2 as cv
import os
import pandas as pd


if __name__ == '__main__':
    RDK = robolink.Robolink()
    CAM_NAME = 'My Camera'
    CAM_PARAMS = 'SIZE=640x480'
    WINDOW_NAME = 'My Camera Feed'
    BASE_PATH = '/Users/akshitshishodia/tracker/roboDK /test2/test'
    data = pd.DataFrame(columns=['name','joint_pose'])
    cnt = 0 


    inventory = RDK.Item('inventory')
    cam_item = RDK.Item(CAM_NAME, robolink.ITEM_TYPE_CAMERA)
    if not cam_item.Valid():
        cam_item = RDK.Cam2D_Add(RDK.AddFrame(CAM_NAME + ' Frame'), CAM_PARAMS)
        cam_item.setName(CAM_NAME)
    cam_item.setParam('Open', 1)

    while cam_item.setParam('isOpen') == '1':

        img_socket = None
        bytes_img = RDK.Cam2D_Snapshot('', cam_item)
        joint_pose = inventory.Joints()

        if isinstance(bytes_img, bytes) and bytes_img != b'':
            nparr = np.frombuffer(bytes_img, np.uint8)
            img_socket = cv.imdecode(nparr, cv.IMREAD_COLOR)
        if img_socket is None:
            break
        name = str(cnt)+ ".png"
        path = os.path.join(BASE_PATH,name)
        cv.imwrite(path,img_socket)
        data = data.append({'name':name,'joint_pose':joint_pose[0][0]},ignore_index = True)
        data.to_csv("name_and_pose2.csv")
        cnt+=1
        cv.imshow(WINDOW_NAME, img_socket)



    cv.destroyAllWindows()
    RDK.Cam2D_Close(cam_item)
