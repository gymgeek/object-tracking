import cv2
import imutils
import serial
from serial_utils import serial_ports


def view_on_ledstrip(rects):
    for x, y, w, h in rects:
        cx, cy = x + w/2, y + h/2
        led_number = int((cx / WIDTH) * NUMBER_OF_LEDS)
        if led_number == NUMBER_OF_LEDS:
            led_number = NUMBER_OF_LEDS - 1

        s.write(bytes(chr(led_number), "utf-8")) 

NUMBER_OF_LEDS = 90
WIDTH = 640

s = serial.Serial(serial_ports()[0], 9600)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


    view_on_ledstrip(faces)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    frame = imutils.resize(frame, width=900)
    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
