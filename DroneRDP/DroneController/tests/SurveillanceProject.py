import KeyPressModule as kp
from djitellopy import tello as tel
import time
from time import sleep
import cv2

# Initialization
kp.init()
tello = tel.Tello()
tello.connect()
print(tello.get_battery())
global img
tello.streamon()


# Function that gets the keyboard inputs
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

    if kp.getKey("p"):
        cv2.imwrite(f'../Resources/Images/{time.time()}.jpg', img)
        sleep(0.3)

    return [lr, fb, ud, yv]


while True:
    try:
        vals = getKeyboardInput()
        tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    except:
        # An error occurred so do nothing as a fallback
        # Maybe do an emergency landing?
        print("error occurred")
        tello.send_rc_control(0, 0, 0, 0)

    # Gets the video from the drone
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    sleep(0.05)
