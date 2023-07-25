import serial
import time

# Arduino'ya bağlanacak seri port ve baud rate
serial_port = 'COM5'
baud_rate = 9600

# Seri haberleşme başlat
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # Arduino'nun başlangıç için hazırlanması için kısa bir bekleme süresi



def send_command(servo_num, angle):
    # Servo numarası ve açı değerini Arduino'ya gönder
    command = f'{servo_num}:{angle}\n'
    ser.write(command.encode())

# Örnek kullanım
while True:
    servo_num = int(input("Servo numarasını girin (1 veya 2): "))
    if servo_num not in (1, 2):
        print("Geçersiz servo numarası! Lütfen 1 veya 2 girin.")
        continue

    angle = int(input("Açı değerini girin (0 ile 180 arasında): "))
    if angle < 0 or angle > 180:
        print("Geçersiz açı değeri! Lütfen 0 ile 180 arasında bir değer girin.")
        continue

    send_command(servo_num, angle)
