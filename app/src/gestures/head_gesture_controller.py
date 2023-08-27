import cv2
import mediapipe as mp
import time
import threading


def angle_limit(value, min_value, max_value):  # Açıyı 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class HeadGestureController:
    def __init__(self, serial_com):
        self.serial_com = serial_com
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.face_mesh = self.mpFaceMesh.FaceMesh()
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.thread_lock = threading.Lock()

    def send_command(self, servo_num, angle, direction):  # Servo numarası ve açı değerini Arduino'ya gönder
        with self.thread_lock:
            angle1 = angle_limit(angle, 40, 130)
            command = f'{servo_num}:{angle1}:{direction}\n'
            if self.serial_com:
                self.serial_com.write(command.encode())

        print("kafa icin komut gönderildi")

    def process_gestures(self, imgRGB, frame):
        results = self.face_mesh.process(imgRGB)
        results2 = self.pose.process(imgRGB)
        lmList = []

        if results.multi_face_landmarks:
            # if results2.pose_landmarks:
            #     self.mpDraw.draw_landmarks(frame, results2.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            for id, lm in enumerate(results2.pose_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])



            # if not results2.pose_landmarks:
            #     pass

            for landmarks in results.multi_face_landmarks:
                nose_landmark = landmarks.landmark[5]  # Burun noktasının indeksi

                h, w, _ = frame.shape

                nose_x, nose_y = int(nose_landmark.x * w), int((nose_landmark.y * h))

                arm_x, arm_y = lmList[11][1:]

                fark_x = arm_x - nose_x
                angle_left_right = int((fark_x / 480) * 160)


                fark_y = arm_y - nose_y
                angle_up_down = int((fark_y / 420) * 160)


                self.send_command(0, angle_left_right,2)
                self.send_command(1, angle_up_down,2)

                # Burunu işaretlemek için daire çiz
                cv2.circle(frame, (nose_x, nose_y), 10, (255, 0, 255), -1)


        if not results.multi_face_landmarks:
            cv2.putText(frame, "yuzsuz", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.send_command(0, 90, 1)
            self.send_command(1, 90, 1)
