# Tello Drone basic movement file
# Created By: Gavin Kuehn
# Version: DroneController 0.0.2
# 10/16/23

from djitellopy import tello
from time import sleep

# Connect to the drone
me = tello.Tello()
me.connect()
print(me.get_battery())
