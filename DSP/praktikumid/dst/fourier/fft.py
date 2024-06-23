#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from dst.math.roots_of_unity import roots_of_unity


def fft(input_signal):
    """
    See funktsioon võtab sisendiks ajadomeenis oleva signaali
    ning rakendab sellel Fourier' kiirteisendust.

    Sisendid:
    input_signal: signaal ajadomeenis (pikkus on 2 aste)

    Tagastab:
    output: kompleksarvuline järjend sageduskomponentidest
    """

    assert 2 ** np.floor(np.log2(len(input_signal))) == len(input_signal), "Signaali pikkus peab olema 2 aste"

    # 1. Väärtustage alamtehete tulemused. Selleks kutsuge vajadusel funktsioon rekursiivselt välja.

    # 2. Leidke abimuutujad tulemuste kombineerimiseks (õige astme kompleksjuured).

    # 3. Kombineerige tulemused vastavalt eeskirjale.

    # 4. Tagastage (alam)tulemus.
    #kasutasin seda allikat https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.03-Fast-Fourier-Transform.html

    N = len(input_signal)

    # ühe elemendi Fourier' teisendus on element ise.
    if N == 1:
        return np.array(input_signal)
    else:
        paaris = fft(input_signal[::2])
        #print("minu paar", paaris)
        paaritu = fft(input_signal[1::2])
        #print("minu paaritu", paaritu)
        #print("NINA", N)
        factor = roots_of_unity(N)
        #print("N-factor", N)
        #print("factorrrrrrrr", factor)
        # täisarv
        #print("factuuu", factor[:N//2])
        #print(paaritu)
        vastus = np.concatenate([paaris+factor[:N//2]*paaritu, paaris+factor[N//2:]*paaritu])
        #print("vastus: ", vastus)
        #
    return vastus


def ifft(input_signal):
    """
    See funktsioon võtab sisendiks sagedusruumis oleva kompleksarvulise signaali
    ning teostab sellele Fourier' pöördteisenduse, kasutades kiirteisendust.

    Sisendid:
    input_signal: kompleksarvuline signaal sagedusruumis (pikkus on 2 aste)

    Tagastab:
    output: reaalarvuline järjend signaalist ajadomeenis
    """

    assert 2 ** np.floor(np.log2(len(input_signal))) == len(input_signal), "Signaali pikkus peab olema 2 aste"

    #print("enne kompleksi", input_signal)
    #input_signal = np.asarray(input_signal, dtype = complex)
    #print("pärast kompleksi", input_signal)
    # sagedusdomeeni signaal tagasi ajadomeeni
    signaali_konjugate = np.conjugate(input_signal)
    #print("pärast signaali konju", signaali_konjugate)
    # Andke leitud väärtused sisendiks oma FFT funktsioonile.
    fft_vastus = fft(signaali_konjugate)
    #print("fft es käimist", fft_vastus)

    # Leidke FFT väljundi kaaskompleks.
    kaaskompleks = np.conjugate(fft_vastus)
    # Jätke alles kaaskompleksi reaalarvuline osa.
    #print("a", kaaskompleks)
    reaalosa = np.real(kaaskompleks)
    #print("b", reaalosa)
    # Korrutage saadud reaalarvuline järjend arvuga 1/N
    # ajadomeenis olev signaal oleks õige amplituudiga, mis on võrdne algse signaali amplituudiga
    vastusifft = reaalosa * 1/len(input_signal)
    #print("c", vastusifft)

    return vastusifft
