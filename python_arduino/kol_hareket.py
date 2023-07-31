import threading
import cv2
import time
import mediapipe as mp
import math


class ArmGestureController:
    def __init__(self, ser):
        self.ser = ser
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mpDraw = mp.solutions.drawing_utils
        self.thread_lock = threading.Lock()

    def angle_limit(self, value, min_value, max_value):  # aciyi 0 ile 180 derece arasında sınırlandırır
        return min(max(value, min_value), max_value)

    def send_command(self, servo_num, anglee):
        # Servo numarası ve açı değerini Arduino'ya gönder

        with self.thread_lock:
            command = f'{servo_num}:{anglee}\n'
            self.ser.write(command.encode())

    def findAngle(self, img, p1, p2, p3, lmList, draw=True):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))  # açı hesaplama
        if angle < 0: angle += 360

        angle = int(angle)
        # cv2.putText(img, str(int(angle)), (x2-40, y2+40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        return angle

    def process_gestures(self, imgRGB, img):
        results2 = self.pose.process(imgRGB)

        lmList = []
        if results2.pose_landmarks:
            self.mpDraw.draw_landmarks(img, results2.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            for id, lm in enumerate(results2.pose_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                sag_dirsek = self.findAngle(img, 11, 13, 15, lmList)
                sag_omuz = self.findAngle(img, 13, 11, 29, lmList)
                sol_dirsek = 360 - self.findAngle(img, 12, 14, 22, lmList)
                sol_omuz = 360 - self.findAngle(img, 14, 12, 24, lmList)

                # Açıları sınırlandırın
                sag_dirsek = self.angle_limit(sag_dirsek, 0, 180)
                sag_omuz = self.angle_limit(sag_omuz, 0, 180)
                sol_dirsek = self.angle_limit(sol_dirsek, 0, 180)
                sol_omuz = self.angle_limit(sol_omuz, 0, 180)

                servo_sag_dirsek = 0
                servo_sag_omuz = 1
                servo_sol_dirsek = 2
                servo_sol_omuz = 3

                print(sol_omuz)
                print("---------------------------------------")
                print(sag_dirsek)

                self.send_command(servo_sag_dirsek, sag_dirsek)
                self.send_command(servo_sag_omuz, sag_omuz)
                self.send_command(servo_sol_dirsek, sol_dirsek)
                self.send_command(servo_sol_omuz, sol_omuz)
