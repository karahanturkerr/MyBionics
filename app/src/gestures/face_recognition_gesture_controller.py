import os
import cv2

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


class FaceRecognitionGestureController:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(os.path.join(BASE_DIR, "../../data/model/training.yml"))
        self.cascadePath = os.path.join(BASE_DIR, "../../data/haarcascade_frontalface_default.xml")
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        self.font = cv2.FONT_HERSHEY_TRIPLEX

    def face_now_check(self, img, target_face_id_name: str):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5)

        detected_faces = []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 255), 2)
            face_id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

            target_face_id = "I don't Now You!"

            if face_id == 1:
                target_face_id = target_face_id_name

            detected_faces.append(target_face_id)

            cv2.rectangle(img, (x - 22, y - 90), (x + w + 22, y - 22), (0, 255, 255), 1)
            cv2.putText(img, str(target_face_id), (x - 20, y - 25), self.font, 1, (255, 255, 255), 2)

        return detected_faces
