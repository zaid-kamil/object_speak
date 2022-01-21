## installation 
```shell
pip install -r requirements.txt
```

## run
```
python app.py
```

## Task 1
- *Object-Detection* ✔
- color detection
- text to speech
- database integration


## Common Fixes
Pywintypes error fix
- copy the files (pythoncom38.dll and pywintypes38.dll) from
```shell
C:\Users\"Your user id"\AppData\Roaming\Python\Python38\site-packages\pywin32_system32
```
- To the path:
```shell
C:\Users\"Your user id"\AppData\Roaming\Python\Python38\site-packages\win32\lib
```

## technology
- **opencv** - OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.
- **coco dataset** - The MS COCO (Microsoft Common Objects in Context) dataset is a large-scale object detection, segmentation, key-point detection, and captioning dataset. The dataset consists of 328K images.
- **mobilenet_ssd model** - What is MobileNet-SSD?
MobileNet is a lightweight deep neural network architecture designed for mobiles and embedded vision applications. Single shot object detection or SSD takes one single shot to detect multiple objects within the image.