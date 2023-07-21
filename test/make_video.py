import cv2
import numpy as np
import os
import time
import pandas 
import logging

logging.basicConfig(filename='iou.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)

frameSize = (500, 500)
cnt = 0
data = pandas.read_csv('/Users/akshitshishodia/tracker/roboDK /inventory_path.csv')

BASE_PATH = '/Users/akshitshishodia/tracker/inventoru out'

def get_iou(ground_truth, pred):
    # coordinates of the area of intersection.
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])
     
    # Intersection height and width.
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))
     
    area_of_intersection = i_height * i_width
     
    # Ground Truth dimensions.
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1
     
    # Prediction dimensions.
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1
     
    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection
     
    iou = area_of_intersection / area_of_union
    return iou

for _,row in data.iterrows():

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

    if iou_l>iou_u:
        logging.info("picked lower")
    if iou_u == 0 and iou_l == 0 :
        logging.info("picked neither")
    if iou_u>iou_l :
        logging.info("picking up")


    if cnt == 29:
        break
    name = 'out'+str(cnt)+'.jpg'
    img = cv2.imread(os.path.join('/Users/akshitshishodia/tracker/inventoru out',name))
    img = cv2.rectangle(img,(1383,1428),(1554,1677),(255,0,0),5)
    img = cv2.rectangle(img,(1350,1736),(1569,2078),(0,0,255),5)
    img = cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,230),6)
    cnt+=1
    path = os.path.join(BASE_PATH,name)
    cv2.imshow('fr',img)
    cv2.waitKey(100)

    
cv2.destroyAllWindows()
