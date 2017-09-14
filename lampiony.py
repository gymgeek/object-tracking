import numpy as np
import serial
import cv2
import imutils
import glob
import sys


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


NUMBER_OF_LEDS = 30
WIDTH = 400

#winStride = 8
#padding = 16

winStride = 4
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

def send_detections_to_serial(rects, s):

    for x, y, w, h in rects:
        cx, cy = x + w/2, y + h/2
        led_number = int((cx / WIDTH) * NUMBER_OF_LEDS)
        if led_number == NUMBER_OF_LEDS:
            led_number = NUMBER_OF_LEDS - 1

        s.write(bytes(chr(led_number), "utf-8")) 






if __name__ == '__main__':
    s = serial.Serial(serial_ports()[0], 9600)


    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    #cap=cv2.VideoCapture('vid.avi')
    cap=cv2.VideoCapture(1)
    while True:
        _,frame=cap.read()

        frame = imutils.resize(frame, width=WIDTH)

        found,w=hog.detectMultiScale(frame, winStride=(winStride, winStride), padding=(padding,padding), scale=scale)
        
        send_detections_to_serial(found, s)
        draw_detections(frame,found)
        frame = imutils.resize(frame, width=1200)
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
    cv2.destroyAllWindows()
