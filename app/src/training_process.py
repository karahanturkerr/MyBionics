import os

import cv2
import numpy as np
from PIL import Image

BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))


class TrainingProcess:
    def __init__(self):
        self.cascade_classifier_path: str = os.path.join(BASE_DIR, "../data/haarcascade_frontalface_default.xml")
        self.export_image_path: str = os.path.join(BASE_DIR, "../data/export_image")
        self.model_path: str = os.path.join(BASE_DIR, "../data/model")

        self.detector = cv2.CascadeClassifier(self.cascade_classifier_path)

    def face_detect_data_export(self, face_id: int = 1, vid_cap_source: int = 0):
        # Start capturing video
        vid_cam = cv2.VideoCapture(vid_cap_source)
        # Detect object in video stream using Haarcascade Frontal Face
        # Initialize sample face image
        count = 1

        # Start looping
        while True:
            # Capture video frame
            _, image_frame = vid_cam.read()
            image_frame = cv2.flip(image_frame, 1)
            # Convert frame to grayscale
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            # Detect frames of different sizes, list of faces rectangles
            faces = self.detector.detectMultiScale(gray, 1.3, 5)
            # Loops for each faces
            for (x, y, w, h) in faces:
                # Crop the image frame into rectangle
                cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Increment sample face image
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite(
                    f"{self.export_image_path}/user_{str(face_id)}_{str(count)}.jpg",
                    gray[y:y + h, x:x + w]
                )
                # Display the video frame, with bounded rectangle on the person's face
                cv2.imshow('frame', image_frame)

            # To stop taking video, press 'q' for at least 100ms
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
            # If image taken reach 100, stop taking video
            elif count > 50:
                break

        # Stop video
        vid_cam.release()
        # Close all started windows
        cv2.destroyAllWindows()

    def get_image_and_labels(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        image_paths = [os.path.join(self.export_image_path, f) for f in os.listdir(self.export_image_path)]

        face_samples = []
        ids = []

        # Loop all the file path
        for imagePath in image_paths:

            # Get the image and convert it to grayscale
            pil_image = Image.open(imagePath).convert('L')

            # PIL image to numpy array
            img_numpy = np.array(pil_image, 'uint8')

            # Get the image id
            image_id = int(os.path.split(imagePath)[-1].split("_")[1])
            print(image_id)

            # Get the face from the training images
            faces = self.detector.detectMultiScale(img_numpy)

            # Loop for each face, append to their respective ID
            for (x, y, w, h) in faces:
                # Add the image to face samples
                face_samples.append(img_numpy[y:y + h, x:x + w])
                # Add the ID to IDs
                ids.append(image_id)

        # Get the faces and IDs
        # Train the model using the faces and IDs
        recognizer.train(face_samples, np.array(ids))

        # Save the model into trainer.yml
        recognizer.save(f"{self.model_path}/training.yml")
        # Pass the face array and IDs array
        return face_samples, ids
