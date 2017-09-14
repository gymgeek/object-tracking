import numpy as np
import cv2
import imutils
import serial
from serial_utils import serial_ports


NUMBER_OF_LEDS = 90
WIDTH = 640

s = serial.Serial(serial_ports()[0], 9600)

winStride = 8
padding = 16
scale = 1.05

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def view_on_ledstrip(rects):
    for x, y, w, h in rects:
        cx, cy = x + w/2, y + h/2
        led_number = int((cx / WIDTH) * NUMBER_OF_LEDS)
        if led_number == NUMBER_OF_LEDS:
            led_number = NUMBER_OF_LEDS - 1

        s.write(bytes(chr(led_number), "utf-8"))


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#cap=cv2.VideoCapture('vid.avi')
cap=cv2.VideoCapture(1)
while True:
    _,frame=cap.read()

    frame = imutils.resize(frame, width=WIDTH)

    found,w=hog.detectMultiScale(frame, winStride=(winStride, winStride), padding=(padding,padding), scale=scale)

    view_on_ledstrip(found)

    draw_detections(frame, found)
    cv2.imshow('feed',frame)
    ch = 0xFF & cv2.waitKey(1)
    if ch == 27:
        break
cv2.destroyAllWindows()
