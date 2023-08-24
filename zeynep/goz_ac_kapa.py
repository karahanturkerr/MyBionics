import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import serial

ser = serial.Serial('COM6', 9600)


def send_command(servo_num, angle, direction):  # Servo numarası ve açı değerini Arduino'ya gönder

    command = f'{servo_num}:{angle}:{direction}\n'
    ser.write(command.encode())

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector()
plotY_left = LivePlot(540, 360, [10, 60])
plotY_right = LivePlot(540, 360, [10, 60])

lefteye = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
righteye = [463, 414, 286, 258, 257, 259, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341]

color_left = (0, 0, 255)
color_right = (0, 0, 255)
ratioList_left = []
ratioList_right = []
counter_left = 0
counter_right = 0
blickCounter_left = 0
blickCounter_right = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]

        # Left Eye
        for id in lefteye:
            cv2.circle(img, face[id], 2, color_left, cv2.FILLED)  # çember çizilimi

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]

        lengthVer, _ = detector.findDistance(leftUp, leftDown)  # up down arası mesafe yüzün dikey uzunluğu
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)  # yüzün yatay uzunluğu

        cv2.line(img, leftUp, leftDown, (0, 255, 0), 1)  # yüzün dikey uzunluğu için çizgi
        cv2.line(img, leftLeft, leftRight, (0, 255, 0), 1)  # yüzün yatay uzunluğu için çizgi

        ratio_left = int((lengthVer / lengthHor) * 100)  # yüzün dikey yatay uzunluğu oranı
        ratioList_left.append(ratio_left)  # oran listeye eklenir

        if len(ratioList_left) > 3:  # eğer listenin eleman sayısı üçten fazlaysa listenin başındaki eleman siliniyor
            ratioList_left.pop(0)

        ratioAvg_left = sum(ratioList_left) / len(ratioList_left)  # listesindeki oranların ortalaması hesaplanıyor.

        if ratioAvg_left < 33 and counter_left == 0:
            color_left = (0, 255, 0)
            counter_left = 1
            send_command(1, 70, 1)
            print("sol k gönderildi....")


        elif ratioAvg_left >= 40:
            color_left = (0, 0, 255)
            counter_left = 0
            send_command(1, 90, 1)
            print("sol a gönderildi....")


        # Right Eye
        for id in righteye:
            cv2.circle(img, face[id], 2, color_right, cv2.FILLED)  # çember çizilimi

        rightUp = face[386]
        rightDown = face[374]
        rightLeft = face[362]
        rightRight = face[263]

        lengthVer, _ = detector.findDistance(rightUp, rightDown)  # up down arası mesafe yüzün dikey uzunluğu
        lengthHor, _ = detector.findDistance(rightLeft, rightRight)  # yüzün yatay uzunluğu

        cv2.line(img, rightUp, rightDown, (0, 255, 0), 1)  # yüzün dikey uzunluğu için çizgi
        cv2.line(img, rightLeft, rightRight, (0, 255, 0), 1)  # yüzün yatay uzunluğu için çizgi

        ratio_right = int((lengthVer / lengthHor) * 100)  # yüzün dikey yatay uzunluğu oranı
        ratioList_right.append(ratio_right)  # oran listeye eklenir

        if len(ratioList_right) > 3:  # eğer listenin eleman sayısı üçten fazlaysa listenin başındaki eleman siliniyor
            ratioList_right.pop(0)

        ratioAvg_right = sum(ratioList_right) / len(ratioList_right)  # listesindeki oranların ortalaması hesaplanıyor.

        if ratioAvg_right < 25 and counter_right == 0:
            counter_right = 1
            color_right = (0, 255, 0)
            send_command(0, 90, 1)
            print("sag k gönderildi....")


        elif ratioAvg_right >= 30:
            counter_right = 0
            color_right = (0, 0, 255)
            send_command(0, 50, 1)
            print("sag a gönderildi....")


        imgPlot_left = plotY_left.update(ratioAvg_left, color_left)
        imgPlot_right = plotY_right.update(ratioAvg_right, color_right)

    if not faces:

        send_command(0, 90, 1)
        send_command(1, 70, 1)
        break
    cv2.imshow("img", img)
    cv2.waitKey(1)
