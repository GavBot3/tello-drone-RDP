import tests.KeyPressModule as kp
from djitellopy import tello as tel
from time import sleep

kp.init()
tello = tel.Tello()
tello.connect()
print(tello.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    # LEFT and RIGHT Controls
    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    # Forward and Backward controls
    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    # Up and Down controls
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    # Yaw velocity (turning)
    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yv = -speed

    # Take off and landing
    if kp.getKey("q"):
        tello.land()
    if kp.getKey("e"):
        tello.takeoff()

    if kp.getKey("f"):
        tello.flip_forward()

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
