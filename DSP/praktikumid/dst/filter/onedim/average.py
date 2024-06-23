#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

# Ülesanne 1:
class SMA:
    """
    Klass lihtsa, võrdsete kaaludega liikuva keskmise haldamiseks.
    SMA - Simple moving average.
    """

    def __init__(self, window_size):
        """
        Klassi konstruktor.
        Konstruktoris algväärtustatakse kõik vajalikud isendiväljad.
        Sisendid:
            window_size - Keskmistamisakna suurus. Näitab, mitu viimast elementi keskmistamisel arvesse lähevad.
        """
        self.window_size = window_size  # Kasutame argumendina saadud suurust, et väärtustada vastav isendiväli.
        # TODO: Algväärtustage ka kõik ülejäänud vajalikud isendiväljad. Antud juhul on vaja andmestruktuuri, kuhu koguda eelmiseid andmeid.
        self.window = [] # list kuhu salvestatakse andmed
    def average(self, data_in):
        """
        Arvutab iga lisandunud andmepunkti jaoks uuendatud keskmise keskmistades igal sammul kõik aknasse jäävad elemendid.
        Lisaks uuendab vajaliku(d) isendivälja(d).
        Sisendid:
            data_in - Uus andmepunkt.
        Tagastab:
            data_out - Keskmine, mis on arvutatud akna pealt, kuhu on lisatud uus andmepunkt ja eemaldatud vanim.
        """
        # TODO: Muutke järgnevat rida, teostades korrektne arvutus.
        # Lisame uue ajapunkti aknasse
        self.window.append(data_in)
        # Kui akna suurus on ületatud, eemaldame vanima andmepunkti
        if len(self.window) > self.window_size:
            self.window.pop(0)
        # Arvutame keskmise
        data_out = sum(self.window) / len(self.window)

        return data_out


# Ülesanne 2.1:
class ESMA:
    """
    Klass lihtsa, aga tõhusama võrdsete kaaludega liikuva keskmise haldamiseks.
    ESMA - Efficient simple moving average.
    """

    def __init__(self, window_size):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        """
        Klassi konstruktor.
        Konstruktoris algväärtustatakse kõik vajalikud isendiväljad.
        Sisendid:
            Tuleb ise leida, mida vaja.
        """
        # TODO: Algväärtustage vajalikud isendiväljad.
        self.window_size = window_size  # akna suurus
        self.window = []  # aknas olevad andmed
        self.sum = 0  # summa, mis aitab keskmist arvutada
        pass

    def average(self, data_in):
        """
        Arvutab iga lisandunud andmepunkti jaoks uuendatud keskmise tõhusamal kujul.
        Lisaks uuendab vajaliku(d) isendivälja(d).
        Sisendid:
            data_in - Uus andmepunkt.
        Tagastab:
            data_out - Keskmine, mis on arvutatud akna pealt, kuhu on lisatud uus andmepunkt ja eemaldatud vanim.
        """
        # TODO: Muutke järgnevat rida, teostades korrektne arvutus.
        # Eemalda vanim andmepunkt, kui akna suurus on täis
        if len(self.window) == self.window_size:
            self.sum -= self.window.pop(0)
        # Lisa uus andmepunkt aknasse ja värskenda summat
        self.window.append(data_in)
        self.sum += data_in
        # Arvuta keskmine
        data_out = self.sum / len(self.window)

        return data_out


# Ülesanne 2.2:
class LWMA:
    """
    Klass lineaarselt muutuvate kaaludega liikuva keskmise haldamiseks.
    LWMA - Linearly weighted moving average.
    """

    def __init__(self, window_size):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        """
        Klassi konstruktor.
        Konstruktoris algväärtustatakse kõik vajalikud isendiväljad.
        Sisendid:
            Tuleb ise leida, mida vaja.
        """
        # TODO: Algväärtustage vajalikud isendiväljad.
        self.window_size = window_size
        self.window = []
        self.weights = []
        for i in range(1, self.window_size + 1):
            self.weights.append(i)

    def average(self, data_in):
        """
        Arvutab iga lisandunud andmepunkti jaoks uuendatud lineaarselt kaalutud keskmise.
        Lisaks uuendab vajaliku(d) isendivälja(d).
        Sisendid:
            data_in - Uus andmepunkt.
        Tagastab:
            data_out - Lineaarselt kaalutud keskmine, mis on arvutatud akna pealt,
                kuhu on suurima kaaluga positsioonile lisatud uus andmepunkt
                ja vähima kaaluga positsioonilt eemaldatud vanim.
        """
        # TODO: Muutke järgnevat rida, teostades korrektne arvutus.
        if len(self.window) == self.window_size:
            self.window.pop(0)
        self.window.append(data_in)
        data_out = 0
        for i in range (len(self.window)):
            data_out += self.weights[i]*self.window[i] / sum(self.weights[:len(self.window)])
        return data_out


# Ülesanne 2.3:
class EMA:
    """
    Klass eksponentsiaalselt kahanevate kaaludega liikuva keskmise haldamiseks.
    EMA - Exponential moving average.
    """

    def __init__(self, alpha):  # Konstruktorisse tuleb ise lisada vajalikud argumendid.
        """
        Klassi konstruktor.
        Konstruktoris algväärtustatakse kõik vajalikud isendiväljad.
        Sisendid:
            Tuleb ise leida, mida vaja.
        """
        # TODO: Algväärtustage vajalikud isendiväljad.
        self.alpha = alpha
        self.current_average = None

    def average(self, data_in):
        """
        Arvutab iga lisandunud andmepunkti jaoks uuendatud eksponentsiaalselt kaalutud keskmise.
        Lisaks uuendab vajaliku(d) isendivälja(d).
        Sisendid:
            data_in - Uus andmepunkt.
        Tagastab:
            data_out - Eksponentsiaalselt kaalutud keskmine, mis arvestab varasemate väärtustega vastavalt kaalude jaotusele.
        """
        # TODO: Muutke järgnevat rida, teostades korrektne arvutus.
        if self.current_average is None:
            self.current_average = data_in
        else:
            self.current_average = self.alpha * data_in + (1 - self.alpha) * self.current_average

        return self.current_average


if __name__ == "__main__":
    pass
