import tensorflow
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from segment_anything import SamPredictor,sam_model_registry
model = tensorflow.keras.models.load_model('/Users/akshitshishodia/intern/tracker/files/model_2.h5')
# path = '/Users/akshitshishodia/Desktop/Screen Recording 2023-07-07 at 10.20.02 PM.mov'
cap = cv2.VideoCapture('/Users/akshitshishodia/Desktop/Screen Recording 2023-07-07 at 10.20.02 PM.mov')
sam = sam_model_registry["vit_b"](checkpoint="/Users/akshitshishodia/intern/tracker/sam_vit_b_01ec64.pth")

def convert_frame(frame):
    x = cv2.resize(frame,(512,512))
    x = (x-127.5)/127.5
    x = x.astype(np.float32)
    x = np.expand_dims(x,axis=0)
    return x

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

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
    # frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),thickness=3)

    predictor = SamPredictor(sam)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    predictor.set_image(img)
    input_box = np.array([x1,y1,x2,y2])
    masks, _, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=False,
    )
    # plt.figure(figsize=(10, 10))
    # plt.imshow(img)
    # show_mask(masks[0], plt.gca())
    # show_box(input_box, plt.gca())
    # plt.axis('on')
    idx = np.where(masks[0] == True)
    y = int(idx[0].mean())
    x = int(idx[1].mean())
    y1 = np.max(idx[0])
    x1 = np.max(idx[1])

    y2 = np.min(idx[0])
    x2 = np.min(idx[1])
    frame = cv2.rectangle(frame,(x2,y1),(x1,y2),(0,255,0),5)
    frame = cv2.circle(frame,(x,y),5,(0,255,0),-1)


    cv2.imshow('check',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    

cap.release()
cv2.destroyAllWindows()


