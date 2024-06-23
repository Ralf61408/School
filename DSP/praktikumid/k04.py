#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################################################################################
#                                                                                                 #
#                           NB! Lahenda järgnevad ülesanded eraldi harul.                         #
#                                                                                                 #
###################################################################################################

import numpy as np
from scipy.io.wavfile import write, read
from scipy.io import wavfile
import os, sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtGui




def kodu_2():
    # Üldparameetrid
    # Määrame diskreetimissageduse
    diskreetimissagedus = 44100 # Hz
    # Määrame heli kestvuse, mis on meil 2 sekundit
    heli_kestvus = 2  # sekundites
    amplituud = np.iinfo(np.int16).max # amplituud ja määrame bitisügavuse 16-bit PCM

    # AbiFunktsioon, mis genereerib kuulatava sinusoidse helisignaali
    def genereeri_heli(failinimi, helisagedus, vaiksemaks=None):
        # Sämplite arv 2 sekundi jooksul
        sämpleid = diskreetimissagedus * heli_kestvus
        # Genereerime 2 sekundilise helifaili ehk mahutame 2 sekundi sisse Sämplite arvu
        t_seq = np.linspace(0, heli_kestvus, int(sämpleid), endpoint=False)
        # Loome sinusoidse helisignaali vastava sagedusega
        y = np.sin(2 * np.pi * helisagedus * t_seq) * amplituud

        # Kui on määratud vaiksemaks, siis vähendame amplituudi alates määratud ajahetkest
        if vaiksemaks is not None:
            y[int(len(y)/2):] *= vaiksemaks

        # Salvestame heli WAV-faili
        write(failinimi, diskreetimissagedus, y.astype(np.int16))
    
    # Esimene helifail, genereerimine ning salvestamine wav faili sagedusega 440 Hz
    genereeri_heli("andmed/audio/k04_yl2_1.wav", 440)

    # Teine helifail, genereerimine ning salvestamine wav faili sagedusega 43660 Hz - põhjustab aliasingut, kuna see ületab Nyquist'i sagedust.
    genereeri_heli("andmed/audio/k04_yl2_2.wav", 43660)

    # Kolmas 2 sekundiline helifail, genereerime ning salvestamine wav faili kus helitugevus langeb järsult poole peal. Vähendan aplituudi ühele protsendile.
    genereeri_heli("andmed/audio/k04_yl2_3.wav", 440, vaiksemaks=0.01)
    pass

def lisa_graafik(win, helifail):

     # Kontrollime, kas fail on olemas
    if not os.path.isfile(helifail):
        print(f"Faili {helifail} ei leitud.")
        return
    
    # Loeme heli andmed failist.
    sagedus, heli_andmed = wavfile.read(helifail)
    # Teisendame stereo heli monoks, kombineerides kanalid
    if heli_andmed.ndim > 1:
        heli_andmed = np.mean(heli_andmed, axis=1)

    # Sooritame failile programmaatiliselt Fourier' teisendus
    fourier_teisendus = np.fft.rfft(heli_andmed)
    # Leiame sageduskomponendid vastavalt Fourier' teisendusele
    sagedused = np.fft.rfftfreq(len(heli_andmed), 1 / sagedus)

    # Leiame põhisageduse kui suurima magnituudiga sageduse
    pohi_sagedus = sagedused[np.argmax(np.abs(fourier_teisendus))]
    print(f"Faili {os.path.basename(helifail)} põhisagedus on: {pohi_sagedus} Hz")

    p = win.addPlot(title=f"Fourier teisendus failile {os.path.basename(helifail)}")
    p.plot(sagedused, np.abs(fourier_teisendus), pen="y")
    p.setLabel('left', "Magnituud")
    p.setLabel('bottom', "Sagedus (Hz)")
    p.showGrid(x=True, y=True)

def kodu_3():

    app = QtWidgets.QApplication(sys.argv)

    # Loome kaks akent
    win1 = pg.GraphicsLayoutWidget(show=True, title="Spekter failile Bontempi-B3-C5.wav")
    win2 = pg.GraphicsLayoutWidget(show=True, title="Spekter failile Bontempi-B3-C6.wav")

    # Lisa graafikud
    lisa_graafik(win1, "andmed/audio/Bontempi-B3-C5.wav")
    lisa_graafik(win2, "andmed/audio/Bontempi-B3-C6.wav")

    # Käivita rakenduse sündmuse tsükkel, et aknad jääksid avatuks
    sys.exit(app.exec_())


def main():
    kodu_2()
    kodu_3()


if __name__ == "__main__":
    main()
