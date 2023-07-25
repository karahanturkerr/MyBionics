import cv2
import time
import mediapipe as mp

def angle_limit(value, min_value, max_value): #açıyı 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)

class HandGestureController:
    def __init__(self, video_capture=0, serial_port='COM5', baud_rate=9600):
        self.cap = cv2.VideoCapture(video_capture)
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils
        self.previous_hand = None
        time.sleep(2)

    def process_gestures(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = self.hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    if self.previous_hand is None or handLms != self.previous_hand:
                        self.previous_hand = handLms
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)

                        x, y = handLms.landmark[3].x, handLms.landmark[3].y
                        x1, y1 = handLms.landmark[4].x, handLms.landmark[4].y

                        x2, y2 = handLms.landmark[5].x, handLms.landmark[5].y
                        x3, y3 = handLms.landmark[8].x, handLms.landmark[8].y

                        x4, y4 = handLms.landmark[9].x, handLms.landmark[9].y
                        x5, y5 = handLms.landmark[12].x, handLms.landmark[12].y

                        x6, y6 = handLms.landmark[13].x, handLms.landmark[13].y
                        x7, y7 = handLms.landmark[16].x, handLms.landmark[16].y

                        x8, y8 = handLms.landmark[17].x, handLms.landmark[17].y
                        x9, y9 = handLms.landmark[20].x, handLms.landmark[20].y

                        # Diğer el landmarkları için gerekli işlemleri burada yapabilirsiniz...

                        # Distance hesaplamaları ve açı dönüşümleri
                        distance1 = int((x2 - x) * img.shape[0])
                        distance2 = int((y2 - y3) * img.shape[0])
                        distance3 = int((y4 - y5) * img.shape[0])
                        distance4 = int((y6 - y7) * img.shape[0])
                        distance5 = int((y8 - y9) * img.shape[0])

                        angle1 = int((distance1 / 70) * 170)
                        angle2 = int((distance2 / 150) * 170)
                        angle3 = int((distance3 / 175) * 170)
                        angle4 = int((distance3 / 163) * 170)
                        angle5 = int((distance3 / 133) * 170)

                        angle1 = angle_limit(angle1, 0, 180)
                        angle2 = angle_limit(angle2, 0, 180)
                        angle3 = angle_limit(angle3, 0, 180)
                        angle4 = angle_limit(angle4, 0, 180)
                        angle5 = angle_limit(angle5, 0, 180)

                        print("mesafe 3 : " + str(distance1))
                        print("aci 3 : " + str(angle1))
                        print("------------------------------------------------------------------------")
                        print("mesafe 2 : " + str(distance2))
                        print("aci 2 : " + str(angle2))

            else:
                self.previous_hand = None

            cv2.imshow("img", img)
            cv2.waitKey(1)

# Sınıf örneğini oluşturup işlemi başlatabilirsiniz
controller = HandGestureController()
controller.process_gestures()
