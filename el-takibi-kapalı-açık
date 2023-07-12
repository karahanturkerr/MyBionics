import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpHand = mp.solutions.hands

hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    succes, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            x, y = handLms.landmark[9].x, handLms.landmark[9].y
            x1, y1 = handLms.landmark[12].x, handLms.landmark[12].y

            font = cv2.FONT_HERSHEY_PLAIN

            if y1 > y:
                cv2.putText(img, "KAPALI", (10, 50), font, 4, (0, 0, 0), 3)
            else:
                cv2.putText(img, "ACIK", (10, 50), font, 4, (0, 0, 0), 3)

            for id, lm in enumerate(handLms.landmark):
                print(id, lm)
                h, w, c = img.shape

                cx, cy = int(lm.x*w), int(lm.y*h)

                if id == 0:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "fps: "+str(int(fps)), (5, 105), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)
