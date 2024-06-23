#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from dst.fourier.Phasor import Phasor


def square_wave(term):
    """
    See funktsioon võtab sisendiks, mitmendat ruutsignaali järku praegu arvutatakse
    ning tagastab sellele järgule vastava faasori.
    https://en.wikipedia.org/wiki/Fourier_series#Convergence
    https://www.mathsisfun.com/calculus/fourier-series.html

    Sisendid:
    term: mitmendat ruutsignaali sinusoidaalset komponenti arvutatakse

    Tagastab:
    phasor: Phasor klassi element, mille sisuks on faasori sagedus, magnituud ja faas
    """
    # 3.1 Ülesanne
    # Implementeeri meetod
    # TODO
    # sagedus(vastavalt valemile), magnituud4/pi on konstant ning magnituud väheneb 2*term+1 võrra, faas - ruutsignaali puhul 90 kraadi
    phasor = Phasor(2*term+1, 4/(np.pi*(2*term+1)), np.pi/2)
    return phasor


def create_8like_signal(scaler=50):
    # Ülesanne 4.1
    # Looge endale testsignaal
    # Peab koosnema sajast andmepuktist.
    # Kontrollitakse testidega.
    # TODO
    x = scaler * (np.sin(np.arange(0, 2*np.pi, ((2*np.pi)/100))*2))
    y = scaler * (np.cos(np.arange(0, 2*np.pi, ((2*np.pi)/100))))
    return x, y

