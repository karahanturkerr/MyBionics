import cv2
import mediapipe as mp
import threading


def angle_limit(value, min_value, max_value):  # aciyi 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class MouthGestureController:
    def __init__(self, serial_com):
        self.serial_com = serial_com
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)
        self.thread_lock = threading.Lock()
    def send_command(self, servo_num, angle, direction):  # Servo numarası ve açı değerini Arduino'ya gönder
        with self.thread_lock:
            angle1 = angle_limit(angle, 40, 130)
            command = f'{servo_num}:{angle1}:{direction}\n'
            if self.serial_com:
                self.serial_com.write(command.encode())

        print("agiz icin komut gönderildi")

    def process_gestures(self, rgb_frame, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb_frame)

        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                upper_lip_center_y = face_landmarks.landmark[13].y * h
                lower_lip_center_y = face_landmarks.landmark[14].y * h
                fark = lower_lip_center_y - upper_lip_center_y
                mouth_angle = angle_limit(int((fark/ 40) * 160), 60, 90)
                servo_mouth = 2
                print(mouth_angle)
                self.send_command(servo_mouth,mouth_angle,1)

                cv2.circle(bgr_frame, (int(face_landmarks.landmark[13].x * w), int(upper_lip_center_y)), 4, (0, 255, 0), -1)
                cv2.circle(bgr_frame, (int(face_landmarks.landmark[14].x * w), int(lower_lip_center_y)), 4, (0, 255, 0), -1)


