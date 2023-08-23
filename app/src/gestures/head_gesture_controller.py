import cv2
import mediapipe as mp
import time
import threading


class HeadGestureController:
    def __init__(self, serial_com):
        self.serial_com = serial_com
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection()
        self.mpDraw = mp.solutions.drawing_utils
        self.thread_lock = threading.Lock()

    def angle_limit(self, value, min_value, max_value):  # Açıyı 0 ile 180 derece arasında sınırlandırır
        return min(max(value, min_value), max_value)

    def send_command(self, servo_num, angle):
        # Servo numarası ve açı değerini Arduino'ya gönder
        with self.thread_lock:
            command = f'{servo_num}:{angle}\n'

            if self.serial_com:
                self.serial_com.write(command.encode())

    def process_gestures(self, imgRGB, img):
        results = self.faceDetection.process(imgRGB)

        if results.detections:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(img, bbox, (0, 255, 255), 2)

                # Yüzün merkezini bul
                center_x = bbox[0] + bbox[2] // 2
                center_y = bbox[1] + bbox[3] // 2

                # Ekran genişliği ve yüksekliğini al
                screen_width, screen_height = w, h

                # Yüz merkezinin ekran merkezine göre yatay ve dikey uzaklıklarını hesapla
                x_distance = center_x - screen_width // 2
                y_distance = center_y - screen_height // 2

                servo_kafa_ss = 0
                servo_kafa_ay = 1

                # Hareket yönünü belirle ve Arduino'ya gönder
                if abs(x_distance) > abs(y_distance):
                    if x_distance > 50:
                        movement = "Sag"
                        self.send_command(servo_kafa_ss, self.angle_limit(90 + abs(x_distance), 40, 140))
                        # print(x_distance)
                    elif x_distance < -50:
                        movement = "Sol"
                        self.send_command(servo_kafa_ss, self.angle_limit(90 - abs(x_distance), 40, 140))
                        # print(x_distance)
                    else:
                        movement = "Duz"
                        self.send_command(servo_kafa_ss, 90)
                        print(x_distance)
                else:
                    if y_distance > 70:
                        movement = "Asagi"
                        self.send_command(servo_kafa_ay, self.angle_limit(90 - abs(y_distance), 90, 75))
                        print(y_distance)
                    elif y_distance < -10:
                        movement = "Yukari"
                        self.send_command(servo_kafa_ay, self.angle_limit(90 + abs(y_distance), 90, 120))
                    else:
                        movement = "Duz"
                        self.send_command(servo_kafa_ay, 90)

                cv2.putText(img, f"Hareket: {movement}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
