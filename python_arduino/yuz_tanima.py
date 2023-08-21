import cv2
import numpy as np


class FaceRecognition:
    def __init__(self):

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('deneme/egitim.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath);
        self.font = cv2.FONT_HERSHEY_TRIPLEX

    def process_gestures(self, imgRGB, im, is_now_face=False):

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5)

        detected_faces = []

        for (x, y, w, h) in faces:

            cv2.rectangle(im, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 255), 2)

            Id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

            if Id == 1:
                Id = "Karahan"
            elif Id == 2:
                Id = "karahann"
            else:
                Id = "Unknow"

            detected_faces.append(Id)

            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,255), 1)
            cv2.putText(im, str(Id), (x - 20, y - 25), self.font, 1, (255, 255, 255), 2)

        return detected_faces




