import cv2
import time
import mediapipe as mp
import threading


def angle_limit(value, min_value, max_value):  # aciyi 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class HandGestureController:
    def __init__(self, serial_com=None):
        self.serial_com = serial_com
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(max_num_hands=2)
        self.mpDraw = mp.solutions.drawing_utils
        self.previous_hand = None
        time.sleep(2)
        self.thread_lock = threading.Lock()

    def send_command(self, servo_num, angle, direction):  # Servo numarası ve açı değerini Arduino'ya gönder
        with self.thread_lock:
            command = f'{servo_num}:{angle}:{direction}\n'

            if self.serial_com:
                self.serial_com.write(command.encode())

        print("el icin komut gönderildi")

    def process_gestures(self, imgRGB, img):
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if self.previous_hand is None or handLms != self.previous_hand:
                    self.previous_hand = handLms

                    x_coords = [lm.x * img.shape[1] for lm in handLms.landmark]
                    y_coords = [lm.y * img.shape[0] for lm in handLms.landmark]
                    min_x, max_x = int(min(x_coords)), int(max(x_coords))
                    min_y, max_y = int(min(y_coords)), int(max(y_coords))

                    # Elin tamamını kapsayacak şekilde sınırlayıcı kutu oluştur
                    cv2.rectangle(img, (min_x - 20, min_y - 20), (max_x + 20, max_y + 20), (0, 255, 0), 2)

                    if x_coords[17] > x_coords[5]:
                        hand_side = "Sag"
                    elif x_coords[5] > x_coords[17]:
                        hand_side = "Sol"
                    else:
                        hand_side = None

                    if hand_side:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img, hand_side + " el", (min_x - 70, min_y - 40), font, 1, (255, 255, 255), 2)

                    # elin noktalarının koordinatları hesaplanır
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
                    sag_bas_parmak = int((x2 - x) * img.shape[0])
                    sag_bas_parmak_kisa = int((y - y1) * img.shape[0])
                    sol_bas_parmak = int((x - x2) * img.shape[0])
                    sol_bas_parmak_kisa = int(((y - y1) * img.shape[0]))

                    isaret_parmak = int((y2 - y3) * img.shape[0])
                    orta_parmak = int((y4 - y5) * img.shape[0])
                    yuzuk_parmak = int((y6 - y7) * img.shape[0])
                    serce_parmak = int((y8 - y9) * img.shape[0])

                    # aci ve limitleri belirlendi
                    sag_bas_parmak_angle = angle_limit(170 - int((sag_bas_parmak / 70) * 170), 15, 155)
                    sag_bas_parmak_kisa_angle = angle_limit(int((sag_bas_parmak_kisa / 37) * 170), 15, 155)

                    sol_bas_parmak_angle = angle_limit(int((sol_bas_parmak / 70) * 170), 15, 160)
                    sol_bas_parmak_kisa_angle = angle_limit(int((sol_bas_parmak_kisa / 37) * 170), 15, 155)

                    isaret_parmak_angle = angle_limit(int((isaret_parmak / 150) * 170), 15, 155)
                    orta_parmak_angle = angle_limit(int((orta_parmak / 175) * 170), 15, 155)
                    yuzuk_parmak_angle = angle_limit(int((yuzuk_parmak / 163) * 170), 15, 155)
                    serce_parmak_angle = angle_limit(int((serce_parmak / 133) * 170), 15, 155)

                    print("mesafe: " + str(sag_bas_parmak_kisa))
                    print("aci: " + str(sag_bas_parmak_kisa_angle))

                    # servolar isimlerindirildi
                    servo_sag_bp = 0
                    servo_sag_bp_ks = 1
                    servo_sag_ip = 2
                    servo_sag_op = 3
                    servo_sag_yp = 4
                    servo_sag_sp = 5
                    # servo_sag_omuz = 6
                    # servo_sol_bp = 15
                    # servo_sol_bp_ks = 14
                    # servo_sol_ip = 13
                    # servo_sol_op = 12
                    # servo_sol_yp = 11
                    # servo_sol_sp = 10
                    # servo_sol_omuz = 9

                    self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)

                    if hand_side == "Sag":
                        # print("sag el")
                        # self.send_command(7, 20, 1)
                        # self.send_command(8, 90, 1)
                        # self.send_command(9, 50, 1)
                        # self.send_command(10, 90, 1)

                        self.send_command(servo_sag_bp, sag_bas_parmak_angle, 1)
                        self.send_command(servo_sag_bp_ks, sag_bas_parmak_kisa_angle, 1)
                        self.send_command(servo_sag_ip, isaret_parmak_angle, 1)
                        self.send_command(servo_sag_op, orta_parmak_angle, 1)
                        self.send_command(servo_sag_yp, yuzuk_parmak_angle, 1)
                        self.send_command(servo_sag_sp, serce_parmak_angle, 1)

                    elif hand_side == "Sol":
                        print("sol el")
                        # self.send_command(9, 90, 2)
                        # self.send_command(8, 160, 2)
                        # self.send_command(7, 90, 2)
                        # self.send_command(6, 90, 2)
                        # # self.send_command(servo_sol_omuz, 150, 2)
                        #
                        # self.send_command(servo_sol_bp, sol_bas_parmak_angle, 2)
                        # self.send_command(servo_sol_bp_ks, sol_bas_parmak_kisa_angle, 2)
                        # self.send_command(90, isaret_parmak_angle, 2)
                        # self.send_command(servo_sol_op, orta_parmak_angle, 2)
                        # self.send_command(servo_sol_yp, yuzuk_parmak_angle, 2)
                        # self.send_command(servo_sol_sp, serce_parmak_angle, 2)
                    else:
                        pass

        if not results.multi_hand_landmarks:
            self.send_command(7, 100, 1)
        else:
            self.previous_hand = None
