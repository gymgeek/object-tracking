# object-tracking using OpenCV
This project tries multiple different approaches to track object.
* color tracking
* face tracking
* human body tracking

The tracking itself is accomplished using internal OpenCV mechanisms.

When object is detected, python script than sends horizontal coordinate of the tracked object to arduino over serial line.
Arduino in turn lights up led strip's LED diodes according to object position in camera's field of view.



## Instalation

### OpenCV
http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/


## Configuration
### WebCam seletion
I have 2 webcams and I'm using the external one, but if you have only one webcam, you may want to change this piece of code
```python
camera = cv2.VideoCapture(1)
```
to
```python
camera = cv2.VideoCapture(0)
```


## Running
make sure arduino and webcam is connected and run it! For example:
```python
python3 color_tracking.py
```