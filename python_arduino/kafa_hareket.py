import cv2
import mediapipe as mp
import serial.tools.list_ports
import time

# Seri portu bulma
ser_port = None
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    if 'COM5' in port:
        ser_port = port
        break

if ser_port is None:
    print("COM5 seri portu bulunamadı.")
    exit()

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

# Video akışını başlat
cap = cv2.VideoCapture(0)

# Yüz tespiti için mediapipe kütüphanesini kullan
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()

# Mediapipe çizim yardımcı fonksiyonunu yükle
mpDraw = mp.solutions.drawing_utils

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            cv2.rectangle(frame, bbox, (0, 255, 255), 2)

            # Yüzün merkezini bul
            center_x = bbox[0] + bbox[2] // 2
            center_y = bbox[1] + bbox[3] // 2

            # Ekran genişliği ve yüksekliğini al
            screen_width, screen_height = w, h

            # Yüz merkezinin ekran merkezine göre yatay ve dikey uzaklıklarını hesapla
            x_distance = center_x - screen_width // 2
            y_distance = center_y - screen_height // 2

            # Hareket yönünü belirle ve Arduino'ya gönder
            if abs(x_distance) > abs(y_distance):
                if x_distance > 20:
                    movement = "Sag"
                    send_command(1, angle_limit(90 + abs(x_distance), 0, 180))
                elif x_distance < -20:
                    movement = "Sol"
                    send_command(2, angle_limit(90 + abs(x_distance), 0, 180))
                else:
                    movement = "Duz"
            else:
                if y_distance > 20:
                    movement = "Asagi"
                    send_command(4, angle_limit(90 + abs(y_distance), 0, 180))
                elif y_distance < -20:
                    movement = "Yukari"
                    send_command(5, angle_limit(90 + abs(y_distance), 0, 180))
                else:
                    movement = "Duz"

            cv2.putText(frame, f"Hareket: {movement}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("img", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()