import cv2
import numpy as np
import os
import time
import pandas 
import logging

logging.basicConfig(filename='iou.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
pt = '/Users/akshitshishodia/tracker/test/out'
frameSize = (500, 500)
cnt = 0
data = pandas.read_csv('/Users/akshitshishodia/tracker/roboDK /final_inventory_path_2.csv')
print(data.head())
BASE_PATH = '/Users/akshitshishodia/tracker/roboDK /pred'
data_pose = pandas.read_csv('/Users/akshitshishodia/tracker/name_and_pose.csv')
map_joint = {0:1,45:2,80:3,115:4,150:5,220:6}

def get_iou(ground_truth, pred):
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))
    area_of_intersection = i_height * i_width
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1  
    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection
    iou = area_of_intersection / area_of_union
    return iou

for _,row in data.iterrows():
    if cnt == 294:
        break

    x = int(row.x)
    y = int(row.y)
    x1 = int(x-89/2)
    y1 = y
    x2 = int(x+89/2)
    y2 = int(y+271)
    bbx1 = (x1,y1,x2,y2)
    if cnt==14:
        print(bbx1)
    bbxu = (1383,1428,1554,1677)
    bbxl = (1350,1736,1569,2078)

    iou_l = get_iou(bbxl,bbx1)
    iou_u = get_iou(bbx1,bbxu)
    # logging.info(iou_l) 
    name = str(cnt)+'.png'
    joint_pose = int(float(str(data_pose[data_pose['name']==name].joint_pose).split()[2]))
    img = cv2.imread(os.path.join(BASE_PATH,name))
    text = str(map_joint[joint_pose])+":"



    img = cv2.rectangle(img,(1383,1428),(1554,1677),(255,0,0),5)
    img = cv2.rectangle(img,(1350,1736),(1569,2078),(0,0,255),5)
    img = cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,230),6)
    if iou_l>iou_u:
        logging.info("picked lower")
        text = text + "lower"
        img = cv2.putText(img,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,9,(0,255,0),5)
        path = os.path.join(pt,name)
        cv2.imwrite(path,img=img)


    if iou_u == 0 and iou_l == 0 :
        logging.info("picked neither")
      
    if iou_u>iou_l :
        logging.info("picking up")
    cnt+=1
    cv2.imshow('fr',img)
    cv2.waitKey(100)

    
cv2.destroyAllWindows()
