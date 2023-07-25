import cv2
import time
import mediapipe as mp

def hand_detection():
    cap = cv2.VideoCapture(0)

    mpHand = mp.solutions.hands
    hands = mpHand.Hands()

    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        succes, img = cap.read()
        img = cv2.flip(img, 1)  # Görüntüyü yatay eksende aynalayın
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # El noktalarını al
                x_coords = [lm.x * img.shape[1] for lm in handLms.landmark]
                y_coords = [lm.y * img.shape[0] for lm in handLms.landmark]
                min_x, max_x = int(min(x_coords)), int(max(x_coords))
                min_y, max_y = int(min(y_coords)), int(max(y_coords))

                # Elin tamamını kapsayacak şekilde sınırlayıcı kutu oluştur
                cv2.rectangle(img, (min_x - 20, min_y - 20), (max_x + 20, max_y + 20), (0, 255, 0), 2)

                # Elin yanına metin ekle
                hand_side = "Sag" if x_coords[17] > x_coords[5] else "Sol"
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, hand_side + " el", (min_x - 70, min_y - 40), font, 1, (255, 255, 255), 2)

                mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, "fps: " + str(int(fps)), (5, 105), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("img", img)
        cv2.waitKey(1)
hand_detection()