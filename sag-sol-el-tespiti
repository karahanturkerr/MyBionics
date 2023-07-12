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
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

            # El noktalarını al
            thumb_tip = handLms.landmark[4]  # Başparmak ucu
            index_tip = handLms.landmark[8]  # İşaret parmağı ucu

            # El noktalarının konumunu al
            thumb_x, thumb_y = thumb_tip.x, thumb_tip.y
            index_x, index_y = index_tip.x, index_tip.y

            # Elin sağ veya sol olduğunu belirle
            if thumb_x > index_x:
                hand_side = "Sol"
            else:
                hand_side = "Sag"

            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(img, hand_side + " el", (10, 50), font, 4, (0, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "fps: "+str(int(fps)), (5, 105), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1)
