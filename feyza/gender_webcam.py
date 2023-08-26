from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2
import cvlib as cv
import threading


class GenderDetection:
    def __init__(self):
        # GenderDetection sınıfının başlatıcı metodu
        # Model yükleniyor
        self.model = load_model('gender_detection_with_child.model')

        # Sınıf etiketleri belirleniyor
        self.classes = ['man', 'woman', 'child']

        # Webcam başlatılıyor
        self.webcam = cv2.VideoCapture(0)

        # Çalışan durumu ve thread oluşturma
        self.running = True
        self.thread = threading.Thread(target=self.detect_gender)
        self.thread.start()

    def detect_gender(self):
        # Cinsiyet tespiti işlemini gerçekleştiren metot
        while self.running:
            status, frame = self.webcam.read()
            frame = cv2.flip(frame, 1)

            # Yüz tespiti yapılıyor
            face, confidence = cv.detect_face(frame)

            for idx, f in enumerate(face):
                # Yüz bölgesi alınıyor
                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]

                # Yüzün etrafına dikdörtgen çiziliyor
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # Yüz bölgesi alınıyor
                face_crop = np.copy(frame[startY:endY, startX:endX])

                if (face_crop.shape[0]) < 10 or (face_crop.shape[1]) < 10:
                    continue

                # Görüntü boyutu yeniden boyutlandırılıyor
                face_crop = cv2.resize(face_crop, (96, 96))

                if face_crop is None:
                    print("Yeniden boyutlandırma hatası:", img)
                    continue

                # Görüntü normalize ediliyor
                face_crop = face_crop.astype("float") / 255.0
                face_crop = img_to_array(face_crop)
                face_crop = np.expand_dims(face_crop, axis=0)

                # Cinsiyet tespiti yapılıyor
                conf = self.model.predict(face_crop)[0]
                idx = np.argmax(conf)
                label = self.classes[idx]
                confidence = conf[idx]

                label = "{}: {:.2f}%".format(label, confidence * 100)

                Y = startY - 10 if startY - 10 > 10 else startY + 10

                # Cinsiyet sonucu görüntü üzerine yazdırılıyor
                cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)

            # Sonuçlar görüntüleniyor
            cv2.imshow("gender detection", frame)

            # "Q" tuşuna basıldığında döngü sonlandırılıyor
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Kaynaklar serbest bırakılıyor
        self.webcam.release()
        cv2.destroyAllWindows()

    def stop(self):
        # İşlemi durdurmak için kullanılan metot
        self.running = False
        self.thread.join()


# Sınıfın kullanımı
if __name__ == "__main__":
    # GenderDetection sınıfı örneği oluşturuluyor
    gender_detector = GenderDetection()

    # Kullanıcıdan işlemi durdurması isteniyor
    input("Press Enter to stop...")

    # GenderDetection sınıfının çalışmasını durduruyor
    gender_detector.release_resources()

