import serial, time

def read_data_from_serial(ser: serial.Serial) -> list:

    data = []

    while ser.in_waiting: #Tsükkel töötab seni, kuni pordi puhvrisse on andmeid loetud (s.o. in_waiting väärtus on suurem kui 0).
        line = ser.readline() # Loeb ühe rea puhvrisse kogunenud andmetest.
        if line: # Kontrollib, kas loetud rida ei ole tüh
            string = line.decode().strip() # Dekodeerib loetud baidid stringiks ja eemaldab algusest ja lõpust tühikud.
            num = int(string) # Konverteerib stringi täisarvuks.
            data.append(num/204.6) # Lisab konverteeritud täisarvu jagatuna 204.6-ga listi data.

    return data


def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600) # Loob Serial ühenduse kasutades määratud porti (/dev/ttyUSB0) ja baudi kiirust (9600 bps).

    while True: # Lõputu tsükkel, mis töötab kuni programm lõpetatakse.
        reading = read_data_from_serial(ser) # Kutsub välja read_data_from_serial funktsiooni, et lugeda andmeid Serial pordist ja salvestab tagastatud andmed muutujasse reading.
        print(reading) 
        time.sleep(0.1) #Peatab tsükli 0.1 sekundiks, mis vastab 10 Hz sagedusele (1 sekund / 0.1 sekundit = 10 korda sekundis).


if __name__ == "__main__":
    main()