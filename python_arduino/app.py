import time

import cv2
import serial
from el_kontrol import HandGestureController
from kol_hareket import ArmGestureController
from kafa_hareket import HeadController
from yuz_tanima import FaceRecognition
import cProfile


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


        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
        #     _ = [exec.submit(f, imgRGB, img) for f in func]

        for f in func:
            is_now_face = False

            res = f(imgRGB, img, is_now_face)

            if res and "karahann" in res:
                is_now_face = True
                print(is_now_face)



        # detected_faces = face_recognition.process_gestures(imgRGB, img)
        # print("Algılanan yüzler:", detected_faces)

        cv2.imshow("img", img)
        key = cv2.waitKey(10)
        if key == 27:
            break


if __name__ == "__main__":
    # ser = arduino_connect()

    hand_gesture_controller = HandGestureController()
    # arm_gesture_controller = ArmGestureController(ser=ser)
    # head_gesture_controller = HeadController(ser=ser)
    face_recognition = FaceRecognition()

    profiler = cProfile.Profile()
    profiler.enable()

    # Profillemeyi durdur

    cap = open_camera(func=(
        hand_gesture_controller.process_gestures,
        # arm_gesture_controller.process_gestures,
        # head_gesture_controller.process_gestures,
        face_recognition.process_gestures,
    ))

    profiler.disable()
    profiler.print_stats(sort='cumulative')
