import cv2
import numpy as np
from speak_object import setup
import threading

# print("1. Setting up the TTS engine...")
engine = setup()

object_counter = []
# print("1. Setting up camera...")
engine.say("Setting up camera")

thres = 0.45 # Threshold to detect object
nms_threshold = 0.2
cap = cv2.VideoCapture(0)
cv2.namedWindow( "output", cv2.WINDOW_NORMAL )
cv2.setWindowProperty("output",cv2.WND_PROP_TOPMOST,cv2.WINDOW_GUI_EXPANDEDq)
# cap.set(3,1280)
# cap.set(4,720)
# cap.set(10,150)
 
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
 
# print("2. Setting up Object detection model...")
engine.say("Setting up Object detection model")
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
 
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# print("4. Ready to detect and recognize objects...")
engine.say("Ready to detect and recognize objects...")

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
            item = classNames[classIds[i][0]-1].upper()

            cv2.putText(img,item,(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            text = f'{item} detected'
            if item not in object_counter:
                engine.say(text)
                object_counter.append(item)
            else:
                pass
           
    except:
        pass
    cv2.imshow("output",img)
    engine.runAndWait()
    if cv2.waitKey(1) == ord('q'):
        break
engine.say("I am done detecting objects")
engine.say("Closing the camera")


cap.release()
cv2.destroyAllWindows()

engine.stop()

print("5. Program ended")