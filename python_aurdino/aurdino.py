import serial
import time

# Arduino ile seri bağlantı kur
arduino = serial.Serial('COM5', 9600)  # Arduino'nun bağlı olduğu seri portu ve iletişim hızını ayarlayın
time.sleep(2)  # Arduino'nun başlatılmasını beklemek için bir süre uyuyun

def start_servos():
    command = 'a\n'  # Servo motorları başlatmak için komut gönderina
    arduino.write(command.encode())  # Arduino'ya komutu gönderin
    time.sleep(0.05)  # Arduino'nun komutu işlemesi için bir süre bekleyin

def stop_servos():
    command = 'b\n'  # Servo motorları durdurmak için komut gönderin
    arduino.write(command.encode())  # Arduino'ya komutu gönderin
    time.sleep(0.05)  # Arduino'nun komutu işlemesi için bir süre bekleyin

# Kullanıcıdan input alarak servo motorları kontrol etmek için örnek kullanım
while True:
    user_input = input("Servo motorları başlatmak için 'a', durdurmak için 'b' girin: ")
    if user_input == 'a':
        start_servos()  # Servo motorları başlatmak için
    elif user_input == 'b':
        stop_servos()  # Servo motorları durdurmak için
    else:
        print("Geçersiz giriş!")

# Arduino ile seri bağlantıyı kapat
arduino.close()
