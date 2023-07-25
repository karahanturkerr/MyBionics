import cv2
import time
import mediapipe as mp
import serial
import math

class HandGestureController:
    def __init__(self, serial_port='COM5', baud_rate=9600):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        time.sleep(2)  # Arduino'nun başlangıç için hazırlanması için kısa bir bekleme süresi

    def angle_limit(self, value, min_value, max_value): #açıyı 0 ile 180 derece arasında sınırlandırır
        return min(max(value, min_value), max_value)

    def send_command(self, servo_num, anglee):
        # Servo numarası ve açı değerini Arduino'ya gönder
        command = f'{servo_num}:{anglee}\n'
        self.ser.write(command.encode())

    def findAngle(self, img, p1, p2, p3, lmList, draw=True):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]

        angle = math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2)) #açı hesaplama
        if angle < 0: angle += 360

        angle = int(angle)

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (0, 0, 255), 3)

            cv2.circle(img, (x1, y1), 10,  (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y1), 10, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x3, y1), 10, (0, 255, 255), cv2.FILLED)

            cv2.circle(img, (x1, y1), 15, (0, 255, 255))
            cv2.circle(img, (x2, y2), 15, (0, 255, 255))
            cv2.circle(img, (x3, y3), 15, (0, 255, 255))

            #cv2.putText(img, str(int(angle)), (x2-40, y2+40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        return angle

    def process_gestures(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        mpPose = mp.solutions.pose
        pose = mpPose.Pose()
        mpDraw = mp.solutions.drawing_utils

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results2 = pose.process(imgRGB)

            lmList = []
            if results2.pose_landmarks:
                mpDraw.draw_landmarks(img, results2.pose_landmarks, mpPose.POSE_CONNECTIONS)

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

                    print(sol_omuz)
                    print("---------------------------------------")
                    print(sag_dirsek)

                    self.send_command(0, sag_dirsek)
                    self.send_command(1, sag_omuz)
                    self.send_command(2, sol_dirsek)
                    self.send_command(3, sol_omuz)

            cv2.imshow("image", img)
            cv2.waitKey(1)

if __name__ == "__main__":
    controller = HandGestureController()
    controller.process_gestures()
