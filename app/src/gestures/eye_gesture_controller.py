import threading
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


def angle_limit(value, min_value, max_value):  # Açıyı 0 ile 180 derece arasında sınırlandırır
    return min(max(value, min_value), max_value)


class EyeGestureController:
    def __init__(self, serial_com):
        self.serial_com = serial_com
        self.detector = FaceMeshDetector()
        self.thread_lock = threading.Lock()
        self.counter_left = 0
        self.counter_right = 0

    def send_command(self, servo_num, angle, direction):  # Servo numarası ve açı değerini Arduino'ya gönder
        with self.thread_lock:
            angle1 = angle_limit(angle, 40, 130)
            command = f'{servo_num}:{angle1}:{direction}\n'
            if self.serial_com:
                self.serial_com.write(command.encode())

        print("kafa icin komut gönderildi")

    def process_gestures(self, imgRGB, img):

        img, faces = self.detector.findFaceMesh(img, draw=False)

        plotY_left = LivePlot(540, 360, [10, 60])
        plotY_right = LivePlot(540, 360, [10, 60])

        lefteye = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        righteye = [463, 414, 286, 258, 257, 259, 260, 467, 359, 255, 339, 254, 253, 252, 256, 341]

        color_left = (0, 0, 255)
        color_right = (0, 0, 255)
        ratioList_left = []
        ratioList_right = []


        if faces:
            face = faces[0]

            # Left Eye
            for id in lefteye:
                cv2.circle(img, face[id], 2, color_left, cv2.FILLED)  # çember çizilimi

            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]

            lengthVer, _ = self.detector.findDistance(leftUp, leftDown)  # up down arası mesafe yüzün dikey uzunluğu
            lengthHor, _ = self.detector.findDistance(leftLeft, leftRight)  # yüzün yatay uzunluğu

            # cv2.line(img, leftUp, leftDown, (0, 255, 0), 1)  # yüzün dikey uzunluğu için çizgi
            # cv2.line(img, leftLeft, leftRight, (0, 255, 0), 1)  # yüzün yatay uzunluğu için çizgi

            ratio_left = int((lengthVer / lengthHor) * 100)  # yüzün dikey yatay uzunluğu oranı
            ratioList_left.append(ratio_left)  # oran listeye eklenir

            if len(ratioList_left) > 3:  # eğer listenin eleman sayısı üçten fazlaysa listenin başındaki eleman siliniyor
                ratioList_left.pop(0)

            ratioAvg_left = sum(ratioList_left) / len(ratioList_left)  # listesindeki oranların ortalaması hesaplanıyor.

            if ratioAvg_left < 33:
                color_left = (0, 255, 0)
                self.counter_left = 1
                self.send_command(5, 70, 1)
                print("sol k gönderildi....")


            elif ratioAvg_left >= 40:
                color_left = (0, 0, 255)
                self.counter_left = 0
                self.send_command(5, 90, 1)
                print("sol a gönderildi....")

            # Right Eye
            for id in righteye:
                cv2.circle(img, face[id], 2, color_right, cv2.FILLED)  # çember çizilimi

            rightUp = face[386]
            rightDown = face[374]
            rightLeft = face[362]
            rightRight = face[263]

            lengthVer, _ = self.detector.findDistance(rightUp, rightDown)  # up down arası mesafe yüzün dikey uzunluğu
            lengthHor, _ = self.detector.findDistance(rightLeft, rightRight)  # yüzün yatay uzunluğu

            # cv2.line(img, rightUp, rightDown, (0, 255, 0), 1)  # yüzün dikey uzunluğu için çizgi
            # cv2.line(img, rightLeft, rightRight, (0, 255, 0), 1)  # yüzün yatay uzunluğu için çizgi

            ratio_right = int((lengthVer / lengthHor) * 100)  # yüzün dikey yatay uzunluğu oranı
            ratioList_right.append(ratio_right)  # oran listeye eklenir

            if len(ratioList_right) > 3:  # eğer listenin eleman sayısı üçten fazlaysa listenin başındaki eleman siliniyor
                ratioList_right.pop(0)

            ratioAvg_right = sum(ratioList_right) / len(
                ratioList_right)  # listesindeki oranların ortalaması hesaplanıyor.

            if ratioAvg_right < 25:
                self.counter_right = 1

                self.color_right = (0, 255, 0)
                self.send_command(4, 90, 1)
                print("sag k gönderildi....")


            elif ratioAvg_right >= 30:
                self.counter_right = 0
                color_right = (0, 0, 255)
                self.send_command(4, 50, 1)
                print("sag a gönderildi....")

            imgPlot_left = plotY_left.update(ratioAvg_left, color_left)
            imgPlot_right = plotY_right.update(ratioAvg_right, color_right)

        if not faces:
            self.send_command(0, 90, 1)
            self.send_command(1, 70, 1)