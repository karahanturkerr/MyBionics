import cv2
import serial
import concurrent.futures
from el_kontrol import HandGestureController
from kol_hareket import ArmGestureController
from kafa_hareket import HeadController


def arduino_connect():
    serial_port = 'COM5'
    baud_rate = 9600

    # Seri haberleşme başlat
    ser = serial.Serial(serial_port, baud_rate)

    return ser


def open_camera(func: tuple, source=0):
    cap = cv2.VideoCapture(source)
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
            _ = [exec.submit(f, imgRGB, img) for f in func]

        cv2.imshow("img", img)
        cv2.waitKey(10)


if __name__ == "__main__":
    ser = arduino_connect()

    hand_gesture_controller = HandGestureController(ser=ser)
    arm_gesture_controller = ArmGestureController(ser=ser)
    head_gesture_controller = HeadController(ser=ser)

    cap = open_camera(func=(
        hand_gesture_controller.process_gestures,
        arm_gesture_controller.process_gestures,
        head_gesture_controller.process_gestures,
    ))
