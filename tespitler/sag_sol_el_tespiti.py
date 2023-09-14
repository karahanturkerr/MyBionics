import cv2
import time
import mediapipe as mp
import serial

ser = serial.Serial('COM5', 9600)
def send_command(servo_num, angle, direction):
    # Servo numarası ve açı değerini Arduino'ya gönder
    command = f'{servo_num}:{angle}:{direction}\n'
    ser.write(command.encode())
def hand_detection():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    mpHand = mp.solutions.hands
    hands = mpHand.Hands()

    mpDraw = mp.solutions.drawing_utils


    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Görüntüyü yatay eksende aynalayın
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(imgRGB)

        aci = 90
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                x_coords = [lm.x * img.shape[1] for lm in handLms.landmark]
                y_coords = [lm.y * img.shape[0] for lm in handLms.landmark]
                min_x, max_x = int(min(x_coords)), int(max(x_coords))
                min_y, max_y = int(min(y_coords)), int(max(y_coords))

                cv2.rectangle(img, (min_x - 20, min_y - 20), (max_x + 20, max_y + 20), (0, 255, 0), 2)

                # Bilek noktasının koordinatlarını al
                wrist_x = handLms.landmark[mpHand.HandLandmark.WRIST].x * img.shape[1]
                wrist_y = handLms.landmark[mpHand.HandLandmark.WRIST].y * img.shape[1]
                x, y= handLms.landmark[0].x, handLms.landmark[0].y

                if wrist_y > y_coords[5]:
                    mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
                    aci1 = int((wrist_x / 1400) * 150)
                    aci2 = int((wrist_x / 1200) * 150)
                    if wrist_x > x_coords[5]:  # Bilek noktasının x koordinatı ile karşılaştırma yapılıyor
                        hand_side = "Sag"
                        print("sag aci : " + str(aci1))
                        print("x değeri : "+ str(wrist_x))
                        send_command(9,aci1,1)
                    else:
                        hand_side = "Sol"
                        print("sol aci : " + str(aci2))



                    #print("paarmak :" + str(x_coords[5]))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, hand_side + " el", (min_x - 70, min_y - 40), font, 1, (255, 255, 255), 2)



        if not results.multi_hand_landmarks:
            print("el yok")



            # font = cv2.FONT_HERSHEY_SIMPLEX
            # #cv2.putText(img, "El tespit edilmedi", (img.shape[1] - 300, 40), font, 1, (255, 255, 255), 2)


        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if key == 27:
            break

hand_detection()
