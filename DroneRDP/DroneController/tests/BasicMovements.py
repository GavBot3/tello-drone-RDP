# Tello Drone basic movement file
# Created By: Gavin Kuehn
# Version: DroneController 0.0.2
# 10/16/23

from djitellopy import tello
from time import sleep

# Connect to the drone
tello = tello.Tello()
tello.connect()
print(tello.get_battery())

tello.takeoff()
# tello.send_rc_control(0, 0, 0, 0)

# tello.send_rc_control(0,50,0,0)
sleep(3)
try:
    tello.flip_forward()
except:
    print("cant flip for whatever reason")

sleep(3)
tello.land()
