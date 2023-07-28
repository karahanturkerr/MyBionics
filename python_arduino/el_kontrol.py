import cv2
import time
import mediapipe as mp
import threading


def angle_limit(value, min_value, max_value):  # aciyi 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class HandGestureController:
    def __init__(self, ser):
        self.ser = ser

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(max_num_hands=2)
        self.mpDraw = mp.solutions.drawing_utils
        self.previous_hand = None

        time.sleep(2)

        self.thread_lock = threading.Lock()

    def send_command(self, servo_num, angle):
        # Servo numarası ve açı değerini Arduino'ya gönder

        with self.thread_lock:
            command = f'{servo_num}:{angle}\n'
            self.ser.write(command.encode())

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

                    # Elin yanına metin ekle
                    hand_side = "Sag" if x_coords[17] > x_coords[5] else "Sol"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, hand_side + " el", (min_x - 70, min_y - 40), font, 1, (255, 255, 255), 2)
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS)

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
                    sol_bas_parmak = int((x - x2) * img.shape[0])
                    isaret_parmak = int((y2 - y3) * img.shape[0])
                    orta_parmak = int((y4 - y5) * img.shape[0])
                    yuzuk_parmak = int((y6 - y7) * img.shape[0])
                    serce_parmak = int((y8 - y9) * img.shape[0])

                    # aci ve limitleri belirlendi
                    sag_bas_parmak_angle = angle_limit(int((sag_bas_parmak / 70) * 170), 0, 180)
                    sol_bas_parmak_angle = angle_limit(int((sol_bas_parmak / 70) * 170), 0, 180)
                    isaret_parmak_angle = angle_limit(int((isaret_parmak / 150) * 170), 0, 180)
                    orta_parmak_angle = angle_limit(int((orta_parmak / 175) * 170), 0, 180)
                    yuzuk_parmak_angle = angle_limit(int((yuzuk_parmak / 163) * 170), 0, 180)
                    serce_parmak_angle = angle_limit(int((serce_parmak / 133) * 170), 0, 180)

                    print("mesafe: " + str(isaret_parmak))
                    print("aci: " + str(isaret_parmak_angle))

                    # servolar isimlerindirildi
                    servo_sag_bp = 0
                    servo_sag_ip = 1
                    servo_sag_op = 2
                    servo_sag_yp = 3
                    servo_sag_sp = 4

                    servo_sol_bp = 0
                    servo_sol_ip = 1
                    servo_sol_op = 2
                    servo_sol_yp = 3
                    servo_sol_sp = 4

                    # sag sol el ayrımı yapılır
                    if hand_side == "Sag":
                        self.send_command(servo_sag_bp, sag_bas_parmak_angle)
                        print("sag elllllllllllllllllllll")
                        self.send_command(servo_sag_ip, isaret_parmak_angle)
                        self.send_command(servo_sag_op, orta_parmak_angle)
                        self.send_command(servo_sag_yp, yuzuk_parmak_angle)
                        self.send_command(servo_sag_sp, serce_parmak_angle)

                    elif hand_side == "Sol":
                        self.send_command(servo_sol_bp, sol_bas_parmak_angle)
                        print(hand_side)
                        self.send_command(servo_sol_ip, isaret_parmak_angle)
                        self.send_command(servo_sol_op, orta_parmak_angle)
                        self.send_command(servo_sol_yp, yuzuk_parmak_angle)
                        self.send_command(servo_sol_sp, serce_parmak_angle)
                    else:
                        # Diğer durumlar için yapmak istediğiniz işlemi burada yapabilirsiniz.
                        pass


        else:
            self.previous_hand = None
