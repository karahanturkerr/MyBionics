import concurrent.futures

import cv2

from app.src.gestures.face_recognition_gesture_controller import FaceRecognitionGestureController
from app.src.gestures.hand_gesture_controller import HandGestureController
from app.utils.base_definitions import CAP_WIDTH, CAP_HEIGHT


class MyBionics:
    def __init__(self):
        self.hand_gesture_controller = HandGestureController()
        self.face_recognition_gesture_controller = FaceRecognitionGestureController()

    def camera(self, func: tuple, source=0):
        cap = cv2.VideoCapture(source)
        cap.set(3, CAP_WIDTH)
        cap.set(4, CAP_HEIGHT)

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            is_detect_face = self.face_recognition_gesture_controller.process_gestures(img_rgb, img, False)

            if len(is_detect_face) > 0:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exec:
                    _ = [exec.submit(f, img_rgb, img, False) for f in func]

            cv2.imshow("img", img)
            key = cv2.waitKey(10)
            if key == 27:
                break

    def start(self):
        self.camera(func=(
            self.hand_gesture_controller.process_gestures,
        ))
