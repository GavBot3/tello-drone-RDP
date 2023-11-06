import math

import cv2

import tests.KeyPressModule as kp
from djitellopy import tello as tel
from time import sleep
import numpy as np

# ################# PARAMETERS coordinate #########################
startCoordinate = 500
fSpeed = 117 / 10  # forward speed in cm/s (15cm/s)
aSpeed = 360 / 10  # angular speed in degrees/s (50deg/s
interval = 0.25  # every 0.25 second to record speed

dInterval = fSpeed * interval
aInterval = aSpeed * interval
#######################################################
# x and y positions and a for current angle
x, y = (startCoordinate, startCoordinate)
a = 0
yaw = 0

kp.init()
tello = tel.Tello()
tello.connect()
print(tello.get_battery())

points = [(0,0), (0,0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aSpeed = 50
    # distance
    d = 0
    global yaw, x, y, a

    # LEFT and RIGHT Controls
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    # Forward and Backward controls
    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    # Up and Down controls
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    # Yaw velocity (turning)
    if kp.getKey("a"):
        yv = aSpeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = -aSpeed
        yaw += aInterval

    # Take off and landing
    if kp.getKey("q"):
        tello.land()
    if kp.getKey("e"):
        tello.takeoff()

    if kp.getKey("f"):
        tello.flip_forward()
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - startCoordinate)/100},{(points[-1][1] - startCoordinate)/100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)

    if(points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(2)
