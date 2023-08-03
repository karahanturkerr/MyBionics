import cv2
import time
import mediapipe as mp
import serial

class HandGestureController:
    def __init__(self, video_capture=0, serial_port='COM5', baud_rate=9600):
        self.cap = cv2.VideoCapture(video_capture)
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils
        self.arduino = serial.Serial(serial_port, baud_rate)
        self.previous_hand = None
        time.sleep(2)

    def start_servo(self, servo_name):
        command = servo_name + '\n'
        self.arduino.write(command.encode())
        #self.arduino.write(str(distance).encode())
        time.sleep(0.0001)

    def stop_servo(self, servo_name):
        command = servo_name + '\n'
        self.arduino.write(command.encode())
        time.sleep(0.0001)

    def process_gestures(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = self.hands.process(imgRGB)

            user_input = ''

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    if self.previous_hand is None or handLms != self.previous_hand:
                        self.previous_hand = handLms
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)

                        x, y = handLms.landmark[2].x, handLms.landmark[2].y
                        x1, y1 = handLms.landmark[4].x, handLms.landmark[4].y

                        x2, y2 = handLms.landmark[5].x, handLms.landmark[5].y
                        x3, y3 = handLms.landmark[8].x, handLms.landmark[8].y

                        x4, y4 = handLms.landmark[9].x, handLms.landmark[9].y
                        x5, y5 = handLms.landmark[12].x, handLms.landmark[12].y

                        x6, y6 = handLms.landmark[13].x, handLms.landmark[13].y
                        x7, y7 = handLms.landmark[16].x, handLms.landmark[16].y

                        x8, y8 = handLms.landmark[17].x, handLms.landmark[17].y
                        x9, y9 = handLms.landmark[20].x, handLms.landmark[20].y

                        distance1 = int((x1 - x) * img.shape[0])
                        distance2 = int((y3 - y2) * img.shape[0])
                        distance3 = int((y5 - y4) * img.shape[0])
                        distance4 = int((y7 - y6) * img.shape[0])
                        distance5 = int((y9 - y8) * img.shape[0])



                        if distance1 < 0:
                            user_input += 'a'
                        else:
                            user_input += 'b'

                        if distance2 < 0:
                            user_input += 'c'
                        else:
                            user_input += 'd'

                        if distance3 < 0:
                            user_input += 'e'
                        else:
                            user_input += 'f'

                        if distance4 < 0:
                            user_input += 'g'
                        else:
                            user_input += 'h'

                        if distance5 < 0:
                            user_input += 'i'
                        else:
                            user_input += 'j'

                        if 'a' in user_input:
                            self.start_servo('a')
                            print("a")
                            print(distance2)

                        if 'b' in user_input:
                            self.stop_servo('b')
                            print("b")

                        if 'c' in user_input:
                            self.start_servo('c')
                            print("c")
                        if 'd' in user_input:
                            self.stop_servo('d')
                            print("d")

                        if 'e' in user_input:
                            self.start_servo('e')
                            print("e")
                        if 'f' in user_input:
                            self.stop_servo('f')
                            print("f")

                        if 'g' in user_input:
                            self.start_servo('g')
                            print("g")
                        if 'h' in user_input:
                            self.stop_servo('h')
                            print("h")

                        if 'i' in user_input:
                            self.start_servo('i')
                            print("i")
                        if 'j' in user_input:
                            self.stop_servo('j')
                            print("j")

                        if not user_input:
                            print("Geçersiz giriş!")

            else:
                self.previous_hand = None

            cv2.imshow("img", img)
            cv2.waitKey(1)

# Sınıf örneğini oluşturup işlemi başlatabilirsiniz
controller = HandGestureController()
controller.process_gestures()
