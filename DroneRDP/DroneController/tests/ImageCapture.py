# Tello Drone image capture basic
# Created By: Gavin Kuehn
# Version: DroneController 0.0.2
# 10/28/23

from djitellopy import tello
from time import sleep
import cv2

# Connect to the drone
tello = tello.Tello()
tello.connect()
print(tello.get_battery())


tello.streamon()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)