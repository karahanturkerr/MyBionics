import cv2
import mediapipe as mp
import serial
import time

#
ser_port = 'COM5'
baud_rate = 9600

# Seri haberleşmeyi başlat
ser = serial.Serial(port=ser_port, baudrate=baud_rate)
time.sleep(2)

def send_command(servo_num, angle):
    # Servo numarası ve açı değerini Arduino'ya gönder
    command = f'{servo_num}:{angle}\n'
    ser.write(command.encode())

def angle_limit(value, min_value, max_value): # Açıyı 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class HeadController:
    def __init__(self, video_capture=0, serial_port='COM5', baud_rate=9600):
        self.cap = cv2.VideoCapture(video_capture)
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection()
        self.mpDraw = mp.solutions.drawing_utils
        time.sleep(0.01)

    def process_gestures(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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

                    servo_kafa_ss = 1
                    servo_kafa_ay = 2

                    # Hareket yönünü belirle ve Arduino'ya gönder
                    if abs(x_distance) > abs(y_distance):
                        if x_distance > 50:
                            movement = "Sag"
                            send_command(servo_kafa_ss, angle_limit(90 + abs(x_distance), 0, 180))
                            #print(x_distance)
                        elif x_distance < -50:
                            movement = "Sol"
                            send_command(servo_kafa_ss, angle_limit(90 - abs(x_distance), 0, 180))
                            #print(x_distance)
                        else:
                            movement = "Duz"
                            send_command(servo_kafa_ss, 90)
                            print(x_distance)
                    else:
                        if y_distance > 70:
                            movement = "Asagi"
                            send_command(servo_kafa_ay, angle_limit(90 + abs(y_distance), 0, 180))
                            print(y_distance)
                        elif y_distance < -10:
                            movement = "Yukari"
                            send_command(servo_kafa_ay, angle_limit(90 - abs(y_distance), 0, 180))
                        else:
                            movement = "Duz"
                            send_command(servo_kafa_ay, 90)

                    cv2.putText(img, f"Hareket: {movement}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("img", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



controller = HeadController()
controller.process_gestures()