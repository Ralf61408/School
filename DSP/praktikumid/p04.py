#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abi.visual.p04_tasks import *
from PyQt5.QtWidgets import QApplication
import os
import sys
from dst.math.complex_math import exponent_to_algebraic
import numpy as np

def create_sinusoid(x, k=1, A=1, phi=0):
    """
    Funktsioon, mis rakendab sisendandmete peal soovitud parameetritega koosinusfunktsiooni.

    Argumendid:
    x -- np.array sisendandmetega
    k -- sinusoidi sagedus ühikutes perioode akna kohta
    A -- sinusoidi amplituud
    phi -- sinusoidi faasinihe radiaanides (nihe x-teljel)

    Tagastab:
        np.array, mis saadakse funktsiooni rakendamisel sisendandmetele
    """
    k = (2 * np.pi) * k # 2pi radiaane - üks täisring
    x = A * np.cos(k*x+phi) # koosinus valem 1 loeng. 
    return x

    ##Diskreetmoonutus 


def signal_sum(signals):
    """
    Funktsioon, mis liidab elementhaaval sisendsignaale.

    Argumendid:
    signals -- np.array liidetavatest signaalidest. NB! Signaalide arv ei ole teada.

    Tagastab:
        np.array, mis saadakse sisendsignaalide elementhaaval liitmise tulemusena
    """
    ## axis=0 1 dimensiooniline signaal
    signal_sum = np.sum(signals, axis=0)
    return signal_sum

"""

1.
Skalaarkorrutise väärtus on negatiivne sellisel juhul, kui nende faasid vastanduvad. Kaks signaali on nagu peegelpildis.
0, kui mõlemad 90kraadiga eri suundades ja üks signaal teise otsas.
270 kraadi ka 0, sest 180* hakkab uuesti peale.



2.
skalaarkorrutis on seda suurem, mida rohkem on signaali punktide arve
ma leian esiteks signaali punktide arvu mõlematel signaalidel.
siis leian mõlema signaali skalaarkorrutise. 
Jagan skalaarkorrutise signaali punktide arvuga.
kui tuleb vastus sama, siis saan öelda, et signaalid on samasugused.

## Erinevate pikkustega signaalid näiteks, saame teha pikema signaali nii pikaks kui lühem signaal, või lisada pikemale signaaline nulle juurde.

3.
Mõlemate signaalide amplituudid muudavad skalaarkorrutise tulemust. Kui esimese signaali amplituud on 1, 
siis skalaarkorrutise on 1 kui teise signaali amplituud on 1. Kui teise signaali amplituud on näiteks 10, siis skalaarkorrutis on ka 10.

"""

def compare_signals(signal1, signal2):
    """
    Funktsioon, mis arvutab kahe signaali kattuvuse skalaarkorrutisena.

    Argumendid:
    signal1, signal2 -- np.array, sisendsignaalid, mille kattuvust arvutatakse

    Tagastab:
        float arvuna signaalide skalaarkorrutise tulemus
    """
     # Arvutab kahe signaali skalaarkorrutise ja normaliseerib selle signaali pikkusega
    funktsioon_dot = np.dot(signal1, signal2) / len(signal2)

    return funktsioon_dot


def find_frequencies(x, y):
    """
    Funktsioon, mis leiab algsignaali komponendid, proovides läbi kõik võimalikud faasid ja sagedused.

    Argumendid:
    x -- ajaväärtused
    y -- algsignaal, mida analüüsitakse

    Tagastab:
        np.array kujuga (x.shape[0], 2), kus on iga sageduse jaoks leitud parim kattuvus ja faasinihe (kraadides), mille juures see esines.
    """
    result = np.zeros((x.shape[0], 2))
    #Sinusoidi amplituud
    A = 1
    for sagedus in range(0, len(x)):
        # Initsialiseerib suurima leitud skalaarkorrutise ja vastava faasi
        korrutis = 0
        faas = 0
        # Itereerib läbi kõik võimalikud faasinurgad (0 kuni 359 kraadi)
        for faasinihke_samm in range(0,360):
            # Loob sinusoidi praeguse sageduse ja faasinihke jaoks
            signaal = create_sinusoid(x, sagedus, A, np.radians(faasinihke_samm))
            #signaal = A*np.cos(sagedus*2*np.pi*x + np.radians(faasinihke_samm))
            # Arvutab skalaarkorrutise antud signaali ja algsignaali vahel
            skalaar_korrutis = compare_signals(y, signaal)
            # Kui praegune skalaarkorrutis on suurem kui eelmine suurim, uuendab väärtused
            if skalaar_korrutis > korrutis:
                korrutis = skalaar_korrutis
                faas = faasinihke_samm
        # Salvestab leitud suurima skalaarkorrutise ja vastava faasinihke tulemuste massiivi
        result[sagedus][0] = korrutis
        result[sagedus][1] = faas
    return result


def frequencies_to_complex(frequency_array):
    """
    Funktsioon, mis teisendab leitud algsignaali komponendid kompleksarvudeks.

    Argumendid:
    frequency_array -- funktsiooni find_frequencies väljund - massiiv magnituud-faas paaridest iga sageduse jaoks

    Tagastab:
        kompleksarvuline np.array kujuga (frequency_array.shape[0]), kus on iga sageduse jaoks vastav kompleksarv algebralisel kujul.
    """
    result = np.zeros(frequency_array.shape[0], dtype=np.complex128)
    ## print("jou: ", result)
   ## print("jou2: ", frequency_array)
    for sagedus in range(0, len(result)):
       ## print("sagedused: ", sagedus)
        result[sagedus] = exponent_to_algebraic(frequency_array[sagedus][0], np.radians(frequency_array[sagedus][1]))
   ## print(result)     
    return result

"""
Eksponentkujus on lihtsam teostada kompleksarvude korrutamist ja jagamist, kuna need operatsioonid taanduvad magnituudide korrutamisele/jagamisele ja faaside liitmisele/lahutamisele

Algebralisel kujul on lihtsam teostada kompleksarvude liitmist või lahutamist, kuna saab lihtsalt liita või lahutada vastavaid reaal- ja imaginaarosasid.
Tehtud.
"""


def main():
    STUDYBOOK_NR = "B31108" # Sisesta siia oma matriklinumber
    TASK_NR = 8           # Uuenda seda muutujat vastavalt ülesandele
    RANDOM_SEED = 20      # Muuda seda numbrit, et genereerida uus juhuslike parameetritega algsignaal

    # Järgnevat koodi *ei ole* vaja muuta.
    x = np.arange(0, 1, 0.005) # Ajaväärtused, mille põhjal arvutakse algsignaal ja signaalikomponendid

    app = QApplication(sys.argv)

    SCRIPT_PATH = os.path.dirname(__file__)
    with open(os.path.join(SCRIPT_PATH, "abi/visual/styles.qss")) as file:
        app.setStyleSheet(file.read())

    task = tasklist[TASK_NR-1](studybook_nr=STUDYBOOK_NR, x=x, subtask=RANDOM_SEED)
    task.ifh.set_component_function(create_sinusoid)
    task.ifh.set_sum_function(signal_sum)
    task.ifh.set_compare_function(compare_signals)
    task.ifh.set_frequency_finder(find_frequencies)
    task.ifh.set_frequency_converter(frequencies_to_complex)
    task.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
