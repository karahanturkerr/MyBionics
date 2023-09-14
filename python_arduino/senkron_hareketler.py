import serial
import time



class ServoController:
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.kx_servo = 15 # kafayı omuzlara doğru yönelten servo
        self.kss_servo = 14 # Kafa sağ sol servo
        #self.kya_servo = 2 # Kafa yukarı aşağı servo
        self.cene = 9
        self.sol_goz_kapagi = 10
        self.sag_goz_kapagi = 12
        self.sol_goz = 11
        self.sag_goz = 13


        self.sag_bas_par_eklem = 0
        self.sag_bas_par = 1
        self.sag_isaret = 2
        self.sag_orta = 3
        self.sag_yuzuk = 4
        self.sag_serce = 5
        self.sag_bilek = 7
        self.sag_dirsek = 8
        self.sag_pazu = 9
        self.sag_omuz_ss = 10
        self.sag_omuz_ya = 11


        self.sol_bas_par_eklem = 1
        self.sol_bas_par = 0
        self.sol_isaret = 5
        self.sol_orta = 4
        self.sol_yuzuk = 2
        self.sol_serce = 3
        self.sol_bilek = 6
        self.sol_dirsek = 7
        self.sol_pazu = 8
        self.sol_omuz = 9


    def reset_funct(self):
        for i in range(2):
            # self.send_command_hizli(self.sag_bas_par_eklem,90,1)
            # self.send_command_hizli(self.sag_bas_par, 90,1)
            # self.send_command_hizli(self.sag_isaret, 90,1)
            # self.send_command_hizli(self.sag_orta, 90,1)
            # self.send_command_hizli(self.sag_yuzuk, 90,1)
            # self.send_command_hizli(self.sag_serce, 90,1)
            # self.send_command_hizli(self.sag_bilek, 90,1)
            # self.send_command_hizli(self.sag_dirsek, 90,1)
            # self.send_command_hizli(self.sag_pazu, 90,1)
            # self.send_command_hizli(self.sag_omuz, 90,1)
            self.send_command_hizli(self.sag_goz_kapagi, 90,1)
            self.send_command_hizli(self.sag_goz, 90,1)
            # self.send_command_hizli(self.sol_bas_par_eklem, 90,2)
            # self.send_command_hizli(self.sol_bas_par, 90,2)
            # self.send_command_hizli(self.sol_isaret, 90,2)
            # self.send_command_hizli(self.sol_orta, 90,2)
            # self.send_command_hizli(self.sol_yuzuk, 90,2)
            # self.send_command_hizli(self.sol_serce, 90,2)
            # self.send_command_hizli(self.sol_bilek, 90,2)
            # self.send_command_hizli(self.sol_dirsek, 90,2)
            # self.send_command_hizli(self.sol_pazu, 90,2)
            # self.send_command_hizli(self.sol_omuz, 90,2)
            self.send_command_hizli(self.sol_goz_kapagi, 90,1)
            self.send_command_hizli(self.sol_goz, 90,1)
            self.send_command_hizli(self.kx_servo, 90,1)
            self.send_command_hizli(self.kss_servo, 90,1)
            #self.send_command_hizli(self.kya_servo, 90,2)




        pass

    def angle_limit(self, value, min_value, max_value):  # Açıyı 0 ile 180 derece arasında sınırlandırır
        return min(max(value, min_value), max_value)
    def send_command(self, servo_num, angle, direction):
        for i in range(2):
            angle1 = self.angle_limit(angle, 20, 150)
            command = f'{servo_num}:{angle1}:{direction}\n'
            self.ser.write(command.encode())
            print(f"{servo_num} - komut gönderildi.")
            time.sleep(0.5)

    def send_command_hizli(self, servo_num, angle, direction,hiz = 0.03):
        for i in range(2):
            angle1 = self.angle_limit(angle, 40, 150)
            command = f'{servo_num}:{angle1}:{direction}\n'
            print(f"{servo_num} - komut gönderildi.")
            self.ser.write(command.encode())
            time.sleep(hiz)

    def send_command_es_zamanli(self, servo_num1,servo_num2, angle, direction1,direction2,hiz = 0.03):
        for i in range(2):
            command = f'{servo_num1}:{angle}:{direction1}\n'
            print(f"{servo_num1} - komut gönderildi.")
            self.ser.write(command.encode())

            command = f'{servo_num2}:{angle}:{direction2}\n'
            print(f"{servo_num1} - komut gönderildi.")
            self.ser.write(command.encode())
            time.sleep(hiz)

    def send_command_gozler(self, servo_num, angle, direction,hiz = 0.03):
        for i in range(2):
            command = f'{servo_num}:{angle}:{direction}\n'
            print(f"{servo_num} - komut gönderildi.")
            self.ser.write(command.encode())
            time.sleep(hiz)

    def yavas_ac_kapa(self,servo_num, angle, direction):
        degree = angle
        for j in range(5):
            #self.send_command(servo_num, degree, direction)
            for i in range(10):
                degree = degree - 5
                self.send_command_hizli(servo_num, degree, direction)
            for i in range(5):
                degree = degree + 5
                self.send_command_hizli(servo_num, degree, direction)

    def yavas_ac(self,servo_num, angle, direction):
        degree = angle
        for j in range(3):
            #self.send_command(servo_num, degree, direction)
            for i in range(5):
                degree = degree + 2
                self.send_command_hizli(servo_num, degree, direction)

    def yavas_kapa(self,servo_num, angle, direction):
        degree = angle
        for j in range(3):
            #self.send_command(servo_num, degree, direction)
            for i in range(6):
                degree = degree - 2
                self.send_command_hizli(servo_num, degree, direction)


    def yan_yan(self):
        #self.reset_funct()
        direction = 1
        degree = 90
        self.send_command_hizli(self.kx_servo, degree, direction)
        for i in range(6):
            degree = degree - 2
            self.send_command_hizli(self.kx_servo,degree,direction)
        for j in range(3):
            self.send_command(self.kx_servo, degree, direction)
            for i in range(12):
                degree = degree + 2
                self.send_command_hizli(self.kx_servo, degree, direction)
            for i in range(12):
                degree = degree - 2
                self.send_command_hizli(self.kx_servo, degree, direction)

        self.send_command_hizli(self.kx_servo, 90, direction)
    def servocuk(self):
        #self.reset_funct()
        servo_num = 0
        direction = 1
        degree = 90
        self.send_command(servo_num, degree, direction)
        for i in range(6):
            degree = degree - 2
            self.send_command(servo_num,degree,direction)
        for j in range(3):
            self.send_command(servo_num, degree, direction)
            for i in range(12):
                degree = degree + 2
                self.send_command_hizli(servo_num, degree, direction)
            for i in range(12):
                degree = degree - 2
                self.send_command_hizli(servo_num, degree, direction)

        self.send_command_hizli(servo_num, 90, direction)
    def kafa_birlesik(self):
        #self.reset_funct()
        direction = 1
        degree = 90
        self.send_command(13, degree, direction)

        for j in range(3):
            self.send_command(13, degree, direction)
            for i in range(12):
                degree = degree + 2
                self.send_command_hizli(13, degree, direction)
            for i in range(12):
                degree = degree - 2
                self.send_command_hizli(13, degree, direction)
        time.sleep(0.3)
        degree = 90
        self.send_command(self.kx_servo, degree, direction)
        time.sleep(0.3)
        direction = 1
        degree = 90
        self.send_command(self.kx_servo, degree, direction)
        for i in range(6):
            degree = degree - 2
            self.send_command_hizli(self.kx_servo,degree,direction)
        for j in range(3):
            self.send_command(self.kx_servo, degree, direction)
            for i in range(12):
                degree = degree + 2
                self.send_command_hizli(self.kx_servo, degree, direction)
            for i in range(12):
                degree = degree - 2
                self.send_command_hizli(self.kx_servo, degree, direction)
        degree = 90
        self.send_command(self.kx_servo, degree, direction)
        time.sleep(0.3)

        #self.reset_funct()
        acik = 110
        kapali = 70
        # Hızlı olan kısım
        for i in range(10):
            degree = degree + 2
            self.send_command_hizli(self.kss_servo,degree,direction)
        for j in range(2):
            for i in range(20):
                degree = degree - 2
                self.send_command_hizli(self.kss_servo, degree, direction)

            for i in range(20):
                degree = degree + 2
                self.send_command_hizli(self.kss_servo, degree, direction)

        for i in range(10):
            degree = degree - 2
            self.send_command_hizli(self.kss_servo,degree,direction)


        # for i in range(2):
        #     self.send_command(self.kss_servo,acik,direction)
        #     self.send_command(self.kss_servo,kapali,direction)
        # tekrar = int((90 - kapali)/5)
        # for i in range(tekrar):
        #     kapali = kapali + 5
        #     self.send_command_hizli(self.kss_servo,kapali,direction)



    def yukari_asagi(self):
        #self.reset_funct()
        direction = 1
        degree = 90
        for i in range(8):
            degree = degree + 5
            self.send_command_hizli(self.kya_servo,degree,direction)
        for i in range(10):
            degree = degree - 5
            self.send_command_hizli(self.kya_servo, degree, direction)
        for i in range(2):
            degree = degree + 5
            self.send_command_hizli(self.kya_servo,degree,direction)

    def sag_sol(self,count = 2):
        #self.reset_funct()
        acik = 110
        kapali = 70
        direction = 1
        # Hızlı olan kısım
        for i in range(count):
            self.send_command(self.kss_servo,acik,direction)
            self.send_command(self.kss_servo,kapali,direction)
        tekrar = int((90 - kapali)/5)
        for i in range(tekrar):
            kapali = kapali + 5
            self.send_command_hizli(self.kss_servo,kapali,direction)

        # degree = 90
        # for i in range(8):
        #     degree = degree - 5
        #     self.send_command_hizli(self.kss_servo,degree,2)
        #
        # for j in range(2):
        #     for i in range(16):
        #         degree = degree + 5
        #         self.send_command_hizli(self.kss_servo,degree,2)
        #
        #     for i in range(16):
        #         degree = degree - 5
        #         self.send_command_hizli(self.kss_servo,degree,2)
        #
        # for i in range(8):
        #     degree = degree + 5
        #     self.send_command_hizli(self.kss_servo, degree, 2)

    def cene_funct(self):
            self.send_command(self.cene,90,1)
            aralik = 80
            for j in range(6):
                for i in range(4):
                    aralik = aralik + 5
                    print(f"kapalı - degree = {aralik} ")
                    self.send_command_hizli(self.cene,aralik,1)
                for i in range(4):
                    aralik = aralik - 5
                    print(f" acik - degree = {aralik} ")
                    self.send_command_hizli(self.cene,aralik,1)

    def gozler_kapama_acma(self):
        #self.reset_funct()
        self.send_command(self.sol_goz_kapagi, 100, 1)
        self.send_command(self.sag_goz_kapagi, 80, 1)
        aralik_sol = 80
        aralik_sag = 100
        for j in range(6):
            for i in range(8):
                aralik_sol = aralik_sol + 5
                aralik_sag = aralik_sag - 5
                print(f"kapalı - degree = {aralik_sag} ")
                print(f"kapalı - degree = {aralik_sol} ")
                self.send_command_hizli(self.sol_goz_kapagi, aralik_sol, 1)
                self.send_command_hizli(self.sag_goz_kapagi, aralik_sag, 1)
            for i in range(8):
                aralik_sol = aralik_sol - 5
                aralik_sag = aralik_sag + 5
                print(f"kapalı - degree = {aralik_sag} ")
                print(f"kapalı - degree = {aralik_sol} ")
                self.send_command_hizli(self.sol_goz_kapagi, aralik_sol, 1)
                self.send_command_hizli(self.sag_goz_kapagi,aralik_sag, 1)

    def sol_goz_kirpma(self):

        aralik = 80
        for i in range(8):
            aralik = aralik + 5
            self.send_command_hizli(self.sol_goz_kapagi,aralik,2)

        for i in range(8):
            aralik = aralik - 5
            self.send_command_hizli(self.sol_goz_kapagi,aralik,2)


    def open_close_sag_el(self):
        acik = 100
        kapali = 30
        self.send_command(self.sag_bilek,120,1)
        self.send_command(self.sag_isaret,kapali,1)
        self.send_command(self.sag_orta, kapali, 1)
        self.send_command(self.sag_yuzuk, kapali, 1)
        self.send_command(self.sag_serce, kapali, 1)
        self.send_command(self.sag_bas_par_eklem, kapali, 1)
        self.send_command(self.sag_bas_par, kapali, 1)

        self.send_command(self.sag_bas_par_eklem, acik, 1)
        self.send_command(self.sag_bas_par, acik, 1)
        self.send_command(self.sag_isaret,acik,1)
        self.send_command(self.sag_orta, acik, 1)
        self.send_command(self.sag_yuzuk, acik, 1)
        self.send_command(self.sag_serce, acik, 1)


    def sol_el_deneme(self):
        acik = 120
        kapali = 30
        time.sleep(1)
        self.send_command(self.sol_bilek, 90, 2)
        self.send_command(self.sol_isaret, kapali, 2)
        self.send_command(self.sol_orta, kapali, 2)
        self.send_command(self.sol_yuzuk, kapali, 2)
        self.send_command(self.sol_serce, kapali, 2)
        #self.send_command(self.sol_bas_par_eklem, kapali + 15, 2)
        #self.send_command(self.sol_bas_par, kapali + 15, 2)
        #self.send_command(self.sol_bas_par_eklem+10, acik, 2)
        #self.send_command(self.sol_bas_par, acik + 10, 2)
        self.send_command(self.sol_isaret, acik, 2)
        self.send_command(self.sol_orta, acik, 2)
        self.send_command(self.sol_yuzuk, acik, 2)
        self.send_command(self.sol_serce, acik, 2)


    def open_close_sol_el(self):
        acik = 120
        kapali = 30
        time.sleep(0.1)
        self.send_command(self.sol_pazu,100,2)
        self.send_command(self.sol_dirsek,90,2)
        self.send_command(self.sol_bilek, 90, 2)
        self.send_command(self.sol_isaret, kapali, 2)
        self.send_command(self.sol_orta, kapali, 2)
        self.send_command(self.sol_yuzuk, kapali, 2)
        self.send_command(self.sol_serce, kapali, 2)
        #self.send_command(self.sol_bas_par_eklem, kapali + 15, 2)
        #self.send_command(self.sol_bas_par, kapali + 15, 2)
        #self.send_command(self.sol_bas_par_eklem+10, acik, 2)
        #self.send_command(self.sol_bas_par, acik + 10, 2)
        self.send_command(self.sol_isaret, acik, 2)
        self.send_command(self.sol_orta, acik, 2)
        self.send_command(self.sol_yuzuk, acik, 2)
        self.send_command(self.sol_serce, acik, 2)


    def sag_el_hizli_open_close(self):
        acik = 120
        kapali = 30
        self.send_command_hizli(self.sag_isaret, kapali, 1)
        self.send_command_hizli(self.sag_orta, kapali, 1)
        self.send_command_hizli(self.sag_yuzuk, kapali, 1)
        self.send_command_hizli(self.sag_serce, kapali, 1)
        self.send_command_hizli(self.sag_bas_par_eklem, acik, 1)
        self.send_command_hizli(self.sag_bas_par, kapali, 1)
        time.sleep(3)
        self.send_command_hizli(self.sag_isaret, acik, 1)
        self.send_command_hizli(self.sag_orta, acik, 1)
        self.send_command_hizli(self.sag_yuzuk, acik, 1)
        self.send_command_hizli(self.sag_serce, acik, 1)
        self.send_command_hizli(self.sag_bas_par_eklem, kapali, 1)
        self.send_command_hizli(self.sag_bas_par, acik, 1)

    def sol_el_hizli_open_close(self):
        acik = 120
        kapali = 30
        self.send_command_hizli(self.sol_isaret, kapali, 2)
        self.send_command_hizli(self.sol_orta, kapali, 2)
        self.send_command_hizli(self.sol_yuzuk, kapali, 2)
        self.send_command_hizli(self.sol_serce, kapali, 2)
        #self.send_command_hizli(self.sol_bas_par_eklem, kapali, 2)
        self.send_command_hizli(self.sol_bas_par, kapali, 2)

        self.send_command_hizli(self.sol_isaret, acik, 2)
        self.send_command_hizli(self.sol_orta, acik, 2)
        self.send_command_hizli(self.sol_yuzuk, acik, 2)
        self.send_command_hizli(self.sol_serce, acik, 2)
        #self.send_command_hizli(self.sol_bas_par_eklem, acik, 2)
        self.send_command_hizli(self.sol_bas_par, acik, 2)

    def run_bayrak_hareket(self):
        acik = 120
        kapali = 30
        # self.send_command(15, 40, 1)
        #
        # self.send_command(self.sag_bas_par_eklem, acik, 1)
        # self.send_command(self.sag_bas_par, acik, 1)
        # self.send_command(self.sag_isaret, acik, 1)
        # self.send_command(self.sag_orta, acik, 1)
        # self.send_command(self.sag_yuzuk, acik, 1)
        # self.send_command(self.sag_serce, acik, 1)
        #
        # time.sleep(3)
        # self.send_command(self.sag_isaret, kapali, 1)
        # self.send_command(self.sag_orta, kapali, 1)
        # self.send_command(self.sag_yuzuk, kapali, 1)
        # self.send_command(self.sag_serce, kapali, 1)
        # self.send_command(self.sag_bas_par_eklem, acik, 1)
        # self.send_command(self.sag_bas_par, kapali, 1)
        self.send_command(14, 80, 1)
        self.send_command(14, 100, 1)
        self.send_command(13, 80, 1)
        self.send_command(13, 90, 1)
        self.send_command(15, 110, 1)
        self.send_command(15, 90, 1)
        self.send_command(14, 90, 1)
        self.send_command(12, 66, 1)
        degree = 90
        for j in range(5):
            self.send_command(14, degree, 1)
            for i in range(6):
                degree = degree - 4
                self.send_command_hizli(14, degree, 1)
            for i in range(6):
                degree = degree + 4
                self.send_command_hizli(14, degree, 1)


        # self.send_command(8, 40, 1)
        # self.send_command(10, 100, 1)
        # self.send_command(8, 90, 1)
        # self.send_command(10, 60, 1)
        # self.send_command(9, 90, 1)
        # self.send_command(8,40,1)
        degree = 60
        for j in range(10):
            self.send_command(self.sag_bilek,degree,1)
            for i in range(12):
                degree = degree + 8
                self.send_command_hizli(self.sag_bilek,degree,1)
            for i in range(12):
                degree = degree - 8
                self.send_command_hizli(self.sag_bilek,degree,1)
        # degree = 90
        # for i in range(6):
        #     degree = degree - 5
        #     self.send_command_hizli(10, degree, 1)
        time.sleep(2)


    def dirsek(self):
        degree2 = 100
        for k in range(5):
            self.send_command(11, degree2, 1)
            for m in range(10):
                degree2 = degree2 + 5
                self.send_command_hizli(11, degree2, 1)
            for m in range(10):
                degree2 = degree2 - 5
                self.send_command_hizli(11, degree2, 1)






    def baslangic_hareketi(self):
        self.sag_sol()
        degree_kss = 90
        degree_kya = 90
        for i in range(9):
            degree_kss = degree_kss - 5
            self.send_command_hizli(self.kss_servo,degree_kss,2)

        for i in range(9):
            degree_kya = degree_kya - 5
            self.send_command_hizli(self.kya_servo,degree_kya,2)

        self.open_close_sag_el()

        for i in range(18):
            degree_kss = degree_kss + 5
            self.send_command_hizli(self.kss_servo,degree_kss,2)

        self.open_close_sol_el()

        for i in range(18):
            degree_kss = degree_kss - 5
            self.send_command_hizli(self.kss_servo,degree_kss,2)

        self.sag_el_hizli_open_close()

        for i in range(18):
            degree_kss = degree_kss + 5
            self.send_command_hizli(self.kss_servo,degree_kss,2)


        self.sol_el_hizli_open_close()

        for i in range(9):
            degree = degree_kya + 5
            self.send_command_hizli(self.kya_servo,degree_kya,2)

        for i in range(9):
            degree_kss = degree_kss + 5
            self.send_command_hizli(self.kss_servo,degree_kss,2)
        # Angle parametresini 40 yazmamdaki amaç
        # iki bileğinde aşağı inmesi hata durumunda dereceler incelenmeli!!!!!!!!!!!!!!!!


        # self.send_command_hizli(self.sag_bilek, 40, 1)
        # self.send_command_hizli(self.sol_bilek, 40, 2)
        #Bu kodda hata alırsak öncelikle bu fonksiyonu silelim ardından yukarıdaki iki satırı yorumdan çıkaralım aynı işlem.
        self.send_command_es_zamanli(self.sag_bilek,self.sol_bilek,40,1,2)

    def close(self):
        self.ser.close()

    # 6 no büyük boyun
    # 2 çene
    # 15 sag göz
    # 12 sol göz

    def deneme(self):


        for i in range(50):
            print("gitti")
            self.send_command(0,30,1)
            self.send_command(14,90,1)
            self.send_command(13,90,1)


            self.yavas_ac(14,90,1)
            self.send_command(14, 90, 1)
            self.yavas_kapa(14,90,1)
            self.send_command(14, 90, 1)
            self.send_command(2, 80, 1)
            self.send_command(2, 60, 1)
            self.yavas_ac(14, 90, 1)
            self.send_command(14, 90, 1)
            self.yavas_kapa(14, 90, 1)
            self.send_command(14, 90, 1)
            self.send_command(2, 80, 1)
            self.send_command(2, 60, 1)
            self.send_command(15, 120, 1)
            self.send_command(12, 66, 1)
            self.send_command(15, 90, 1)
            self.send_command(12, 90, 1)
            # self.yavas_kapa(8, 90, 1)
            #
            # self.yavas_ac(8, 72, 1)
            #
            # self.yavas_kapa(8, 90, 1)


if __name__ == "__main__":
    serial_port = 'COM5'
    baud_rate = 9600
    controller = ServoController(serial_port, baud_rate)

    #controller.run_kol_deneme()
    # controller.run_servos()
    #controller.reset_funct()
    # controller.dirsek()
    #controller.run_bayrak_hareket()

    # controller.yan_yan()
    # time.sleep(1)
    # controller.sag_sol()
    #controller.kafa_birlesik()
    #controller.yukari_asagi()
    #controller.reset_funct()
    #controller.cene_funct()
    #controller.gozler_kapama_acma()
    #controller.deneme()
    #controller.open_close_sag_el()
    #controller.open_close_sol_el()
    #controller.sag_el_hizli_open_close()
    #controller.sol_el_hizli_open_close()
    controller.deneme()
    controller.close()