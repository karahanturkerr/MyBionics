import cv2
import mediapipe as mp
#import serial

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

#ser = serial.Serial('COM5', 9600)

'''def send_command(servo_num, angle, direction):
    command = f'{servo_num}:{angle}:{direction}\n'
    ser.write(command.encode())'''

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            upper_lip_center_y = face_landmarks.landmark[13].y * h
            lower_lip_center_y = face_landmarks.landmark[14].y * h
            fark = lower_lip_center_y - upper_lip_center_y
            print(fark)
            aci = int((fark/ 40) * 160)
            print("********")
            print("aci:"+str(aci))
            #print(upper_lip_center_y, lower_lip_center_y)

            cv2.circle(bgr_frame, (int(face_landmarks.landmark[13].x * w), int(upper_lip_center_y)), 4, (0, 255, 0), -1)
            cv2.circle(bgr_frame, (int(face_landmarks.landmark[14].x * w), int(lower_lip_center_y)), 4, (0, 255, 0), -1)

    cv2.imshow('Üst ve Alt Dudak Merkezleri', bgr_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
