import cv2
import mediapipe as mp
import serial

ser = serial.Serial('COM5', 9600)


def send_command(servo_num, angle, direction):
    # Servo numarası ve açı değerini Arduino'ya gönder
    command = f'{servo_num}:{angle}:{direction}\n'
    ser.write(command.encode())


# Kamera yakalamayı başlat
cap = cv2.VideoCapture(0)
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
face_mesh = mpFaceMesh.FaceMesh()

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(imgRGB)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            nose_landmark = landmarks.landmark[5]  # Burun noktasının indeksi

            h, w, _ = frame.shape
            x, y = int(nose_landmark.x * w), int(460 - (nose_landmark.y * h))

            # Burunu işaretlemek için daire çiz
            cv2.circle(frame, (x, 460-y), 10, (255, 0, 255), -1)

            ss_aci = int((x / 625) * 160)
            ay_aci = int((y / 460) * 160)
            print("ss aci: " + str(ss_aci))
            print("******************************")
            print("ay aci: " + str(ay_aci))
            ss_servo = 1
            ay_servo = 0
            send_command(ss_servo,ss_aci,1)
            send_command(ay_servo, ay_aci, 1)
    if not results.multi_face_landmarks:
        cv2.putText(frame, "yuzsuz", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        send_command(ss_servo, 90, 1)
        send_command(ay_servo, 90, 1)



    cv2.imshow('Nose Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()