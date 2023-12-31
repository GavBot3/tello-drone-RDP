# Tello Drone image capture basic
# Created By: Gavin Kuehn
# Version: DroneController 0.0.6
# 11/09/23
import cv2
import numpy as np
from djitellopy import tello
from time import sleep

# Connect to the drone
tello = tello.Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
tello.takeoff()
tello.send_rc_control(0, 0, 30, 0)
sleep(2.2)


# provide global variables
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("../Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListCenter = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListCenter.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListCenter[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0
    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    # print(error, fb)

    if x == 0:
        speed = 0
        error = 0

    tello.send_rc_control(0, fb, 0, speed)
    return error

# cap = cv2.VideoCapture(1)

while True:
    # _, img = cap.read()
    img = tello.get_frame_read().frame

    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    # print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        tello.land()
        break
