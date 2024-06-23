#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from dst.fourier.Phasor import Phasor
import math


def dft(input_signal):
    """
    See funktsioon võtab sisendiks ajadomeenis oleva reaalarvuliste väärtustega signaali (järjendi või massiivi kujul)
    ning rakendab sellel diskreetset Fourier' teisendust.

    Sisendid:
    input_signal: reaalarvuline signaal ajadomeenis

    Tagastab:
    output: järjend klassi Phasor sageduskomponentidest
    """
    print("minu signaal: ", input_signal)
    #sisendsignaalide elementide arv
    signaalide_kogus = len(input_signal)
    print("signaalide kogus", signaalide_kogus)
    #indeksid
    sagedused = np.arange(0, signaalide_kogus, 1)
    print("sagedused", sagedused)
    output = []

    for x_k in sagedused:
        avaldis_summa = 0
        for n in range(0, signaalide_kogus):
            sin = np.sin((2*np.pi*x_k*n)/signaalide_kogus)
            cos = np.cos((2*np.pi*x_k*n)/signaalide_kogus)
            väärtus = input_signal[n] * complex(cos, -sin)
            avaldis_summa += väärtus
        
        #avaldis = (1/signaalide_kogus)*avaldis_summa
        #print("avaldis2", avaldis)
        # Arvutab komplekse arvu magnituudi
        avaldis_magnituud = math.sqrt(avaldis_summa.real**2 + avaldis_summa.imag**2)
        # Arvutab komplekse arvu faasi (nurka) radiaanides
        avaldis_faas = (np.angle(avaldis_summa))

        
        "phasor: Phasor klassi element, mille sisuks on faasori sagedus, magnituud ja faas"

        output.append(Phasor(x_k, avaldis_magnituud, avaldis_faas, avaldis_summa.real, avaldis_summa.imag))
    return output


def idft(input_signal):
    """
    See funktsioon võtab sisendiks 1D järjendi klassi Phasor sageduskomponentidest
    ning rakendab neil diskreetset Fourier' pöördteisendust.

    Sisendid:
    input_signal: järjend klassi Phasor sageduskomponentidest

    Tagastab:
    output: reaalarvuline signaali järjend ajadomeenis
    """

    
    output = []
    ## kogus signaale, palju on
    signaalide_kogus = len(input_signal)
    print("minu sagedused kokku_i", signaalide_kogus)
    ## annan igale signaalile mingi ühiku 1-292 ntks
    sagedused = np.arange(0, signaalide_kogus, 1)
    print("minu sagedused_i", sagedused)

    for x_n in sagedused:
        reaal_väärtused_kokku = 0
        imag_väärtused_kokku = 0
        for x in range(0, signaalide_kogus):
            real = input_signal[x].real * (complex(np.cos(2*np.pi*x_n*x/signaalide_kogus), 1j * np.sin(2*np.pi*x_n*x/signaalide_kogus)))
            imag = input_signal[x].imag * 1j * (complex(np.sin(2*np.pi*x_n*x/signaalide_kogus) * 1j, np.cos(2*np.pi*x_n*x/signaalide_kogus)))
            reaal_väärtused_kokku += real
            imag_väärtused_kokku +=imag

        lõpp_vastus = reaal_väärtused_kokku + imag_väärtused_kokku
        y = lõpp_vastus.real
        np.array(output.append(y/signaalide_kogus))

    return output
    

def magnituudid_faasid(local_dft):
    magnituudid = []
    faasid = []
    ##a = local_dft[0]
    ##b = a.magnitude
    ##c = a.phase

    for x in local_dft:
        magnituudid.append(x.magnitude)
        faasid.append(x.phase)
    
    array_magnituudid = np.array(magnituudid)
    array_faasid = np.array(faasid)
    #print("array_magnituudid", array_magnituudid)
    #print("array_faasid", array_faasid)


    return array_magnituudid, array_faasid
