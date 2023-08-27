import concurrent.futures

import cv2

from config import Config
from src.gestures.eye_gesture_controller import EyeGestureController
from src.gestures.hand_gesture_controller import HandGestureController
from src.gestures.head_gesture_controller import HeadGestureController
from src.gestures.mouth_gesture_controller import MouthGestureController
from utils.base_definitions import CAP_WIDTH, CAP_HEIGHT, BOUND_RATE, SERIAL_PORT
import serial

config = Config()


class MyBionics:
    def __init__(self):

        self.serial_com = None
        self.arduino_connect()

        self.eye_gesture_controller = EyeGestureController(serial_com=self.serial_com)
        self.hand_gesture_controller = HandGestureController(serial_com=self.serial_com)
        self.head_gesture_controller = HeadGestureController(serial_com=self.serial_com)
        self.mouth_gesture_controller = MouthGestureController(serial_com=self.serial_com)

    def arduino_connect(self):
        self.serial_com = serial.Serial(SERIAL_PORT, BOUND_RATE)

    def camera(self, func: tuple, source=0):
        cap = cv2.VideoCapture(source)
        cap.set(3, CAP_WIDTH)
        cap.set(4, CAP_HEIGHT)

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
                _ = [exec.submit(f, img_rgb, img) for f in func]

            cv2.imshow("img", img)
            key = cv2.waitKey(10)
            if key == 27:
                break

    def start(self):
        self.camera(func=(
            #self.hand_gesture_controller.process_gestures,
            self.head_gesture_controller.process_gestures,
            #self.eye_gesture_controller.process_gestures,
            #self.mouth_gesture_controller.process_gestures,
        ))
