import cv2
import numpy as np
from speak_object import TTSThread
from color_detector import getColorName
import queue


# create function to seperated foreground and background from image
def seperate_foreground_background(image):
    # convert image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur the image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # apply threshold
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
    # find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # create empty array to store foreground and background
    foreground = np.zeros(image.shape, np.uint8)
    background = np.zeros(image.shape, np.uint8)
    # loop over contours
    for cnt in contours:
        # get area of contour
        area = cv2.contourArea(cnt)
        # if area is greater than 50 pixels, it will be considered as foreground
        if area > 50:
            cv2.drawContours(foreground, [cnt], 0, (255, 255, 255), -1)
        else:
            cv2.drawContours(background, [cnt], 0, (255, 255, 255), -1)
    return foreground, background

# crop image by mask
def crop_image(im, mask):
    final =  cv2.bitwise_and(im, mask)
    return final



q = queue.Queue()
tts_thread = TTSThread(q)

# print("1. Setting up the TTS engine...")

object_counter = []
# print("1. Setting up camera...")
q.put("starting up camera")

thres = 0.45 # Threshold to detect object
nms_threshold = 0.2
cap = cv2.VideoCapture(0)
cv2.namedWindow( "output", cv2.WINDOW_NORMAL )
cv2.setWindowProperty("output",cv2.WND_PROP_TOPMOST,cv2.WINDOW_GUI_EXPANDED)
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,150)
 
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
 
# print("2. Setting up Object detection model...")
q.put("Started up Object detection model")
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
 
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# print("4. Ready to detect and recognize objects...")
q.put("Ready to detect and recognize objects...")

while True:
    success,img = cap.read()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    bbox = list(bbox)
    item = text = ''
    try:
        confs = list(np.array(confs).reshape(1,-1))
        confs = list(map(float,confs))
        #print(type(confs[0]))
        #print(confs)
    
        indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
        #print(indices)
    
        for i in indices:
            i = i[0]
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            cv2.rectangle(img, (x,y),(x+w,h+y), color=(255, 255, 0), thickness=4)
            crop_img = img[y:y+h, x:x+w]
            cv2.imshow(item,crop_img)
            mask,_ = seperate_foreground_background(crop_img)
            crop_img  = crop_image(crop_img,mask)       
            mean_red = np.mean(crop_img[:,:,2])
            mean_green = np.mean(crop_img[:,:,1])
            mean_blue = np.mean(crop_img[:,:,0])
            color = getColorName(mean_red,mean_green,mean_blue)
            item = classNames[classIds[i][0]-1].upper()

            cv2.putText(img,f"{color} {item}",(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
            text = f'{item} detected of color {color}'
            if item not in object_counter:
                q.put(text)
                object_counter.append(item)
            else:
                pass
           
    except:
        pass
    cv2.imshow("output",img)
   
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()