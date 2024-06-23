#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
import scipy.signal as signal

from abi.visual.plot_image import plot_image

def plot_filter_time(plot_item: pg.graphicsItems.PlotItem, data: np.ndarray) -> None:
    """
    Funktsioon, mis kuvab filtrit aegruumis.

    Argumendid:
    plot_item   -- graafiku objekt, kuhu tuleb filter kuvada
    data        -- filtri kernel aegruumis

    Tagastab:
        None
    """
    # Määrame x-telje skaala ja nime
    plot_item.setLabel('bottom', 'Filtri kerneli elemendi indeks(i)')

    # Määrame y-telje skaala ja nime
    plot_item.setLabel('left', 'Filtri kerneli väärtus')

    # Arvutame x-telje andmed, kasutades arvutatud filtri kerneli pikkust
    x = np.linspace(0, len(data) / 2, len(data))

    # Arvutame y-telje andmed, kasutades arvutatud filtri kerneli väärtusi
    y = data

    # Kuvame graafiku
    plot_item.plot(x, y)
    pass


def plot_filter_freq(plot_item: pg.graphicsItems.PlotItem, data: np.ndarray, dB_scale: bool = False) -> None:
    """
    Funktsioon, mis kuvab filtrit sagedusruumis.

    Argumendid:
    plot_item   -- graafiku objekt, kuhu tuleb filter kuvada
    data        -- filtri kernel sagedusruumis
    dB_scale    -- tõeväärtus, mis väljendab, kas y-telje väärtusi teisendatakse enne kuvamist detsibellidesse.

    Tagastab:
        None
    """
    # Arvutame x-telje andmed, kasutades numpy.linspace()
    x = np.linspace(0, 0.5, len(data))

    # Arvutame y-telje andmed, kasutades filtri kerneli väärtusi
    if dB_scale:
        y = 20 * np.log10(np.abs(data))

        # Määrame x-telje skaala ja nime
        plot_item.setLabel('bottom', 'Sagedus murdosana sämplimiskiirusest')

        # Määrame y-telje skaala ja nime
        plot_item.setLabel('left', 'Filtri võimendus', units='dB')


    else:
        y = np.abs(data)
        # Määrame x-telje skaala ja nime
        plot_item.setLabel('bottom', 'Sagedus murdosana sämplimiskiirusest')

        # Määrame y-telje skaala ja nime
        plot_item.setLabel('left', 'Filtri võimendus')

    # Kuvame graafiku logaritmilises skaalas
    plot_item.plot(x, y, pen='b')
    # plot_item.setLogMode(x=False, y=True)

    pass


def plot_filtered_vs_unfiltered_time(plot_item: pg.graphicsItems.PlotItem, unfiltered_data: np.ndarray, filtered_data: np.ndarray) -> None:
    """
    Funktsioon, mis kuvab filtreerimata ja filtreeritud andmed samal graafikul.

    Argumendid:
    plot_item       -- graafiku objekt, kuhu tuleb andmed kuvada
    unfiltered_data -- filtreerimata andmed
    filtered_data   -- filtreeritud andmed

    Tagastab:
        None
    """

    # Plotime filtreerimata data
    plot_item.plot(x=np.arange(len(unfiltered_data)) / 100000, y=unfiltered_data, pen='b', name='Unfiltered')
    # Plotime filtreeritud data
    plot_item.plot(x=np.arange(len(filtered_data)) / 100000, y=filtered_data, pen='r', name='Filtered')
    pass
    # Seadistan telgede pealkirjad
    plot_item.setLabel('bottom', "Aeg")
    plot_item.setLabel('left', "Magnituud")
    pass


def plot_filtered_vs_unfiltered_freq(plot_item: pg.graphicsItems.PlotItem, unfiltered_data: np.ndarray, filtered_data: np.ndarray) -> None:
    """
    Funktsioon, mis kuvab filtreerimata ja filtreeritud andmete sagedusesitused samal graafikul.

    Argumendid:
    plot_item       -- graafiku objekt, kuhu tuleb sagedusesitused kuvada
    unfiltered_data -- filtreerimata andmed aegruumis
    filtered_data   -- filtreeritud andmed aegruumis

    Tagastab:
        None
    """
    # arvutame fft filtreerimata data-st
    unfiltered_fft = np.abs(np.fft.rfft(unfiltered_data))
    # arvutame sagedusesituse
    #freqs = np.fft.rfftfreq(len(unfiltered_data), d=100000)
    # Plotime filtreerimata andmete sageduse spektri
    plot_item.plot(y=unfiltered_fft, pen='b', name='Filtreerimata signaal')
    # arvutatud FFT filtreeritud andmetest
    filtered_fft = np.abs(np.fft.rfft(filtered_data))
    # Plotime filtreeritud andmete sageduse spektri
    plot_item.plot(y=filtered_fft, pen='r', name='Filtreeritud signaal')

    # Seadistan telgede pealkirjad
    plot_item.setLabel('bottom', "Andmepunkti indeks")
    plot_item.setLabel('left', "Magnituud")
    pass


def plot_spectrogram(plot_item: pg.graphicsItems.PlotItem, data: np.ndarray, noverlap: int = 0, nperseg: int = 1024, sr: int = None) -> None:
    """
    Funktsioon, mis arvutab ja kuvab sisendsignaalist spektrogrammi.

    Argumendid:
    plot_item       -- graafiku objekt, kuhu tuleb spektrogramm kuvada
    data            -- andmed, mille põhjal spektrogramm arvutatakse
    noverlap        -- mitme andmepunkti võrra signaali aknad kattuvad
    nperseg         -- ühe signaalist võetava akna suurus
    sr              -- sämplimissagedus

    Tagastab:
        None
    """
    # Arvutab spektrogrammi kasutades scipy.signal teeki #noverlap: See määrab, kui palju iga järgmine segment eelmisega kattub. #nperseg: See on iga segmendi pikkus, mida kasutatakse Fast Fourier Transform (FFT) arvutamisel spektrogrammi jaoks
    f, t, Sxx = signal.spectrogram(data, fs=sr, nperseg=nperseg, noverlap=noverlap)
    # Arvutab spektrogrammi Sxx amplituudid detsibellides
    Sxx_dB = 20 * np.log10(Sxx)  # Lisa väike number, et vältida logaritmi arvutamist nullist
    # Puhastab graafiku vana sisu
    plot_item.clear()
    # Arvutan dt ja df graafiku telgede õigeks skaleerimiseks, kahe punkti vaheline intervall 
    dt = t[1] - t[0]  # Aja resolutsioon
    df = f[1] - f[0]  # Sageduse resolutsioon

    # Kasutab plot_image funktsiooni, et kuvada spektrogrammi graafikul
    # Siin on vaja täpsustada, mis on plot_image() funktsioon ja kuidas see töötab
    plot_image(plot_item, Sxx_dB, dt, df)

    # Seadistab graafiku telgede sildid, sõltuvalt kas sämplimissagedus on antud või mitte
    if sr is not None:
        plot_item.setLabel('bottom', "Aeg (s)")
        plot_item.setLabel('left', "Sagedus", units="Hz")
    else:
        plot_item.setLabel('bottom', "Andmepunkti indeks")
        plot_item.setLabel('left', "Sagedus murdosana sämplimiskiirusest")

    plot_item.getViewBox().autoRange()



def plot_phase_spectrogram(plot_item: pg.graphicsItems.PlotItem, data: np.ndarray, noverlap: int = 0, nperseg: int = 1024, sr: int = None) -> None:
    """
    Funktsioon, mis arvutab ja kuvab sisendsignaalist faasi spektrogrammi.

    Argumendid:
    plot_item       -- graafiku objekt, kuhu tuleb faasispektrogramm kuvada
    data            -- andmed, mille põhjal faasispektrogramm arvutatakse
    noverlap        -- mitme andmepunkti võrra signaali aknad kattuvad
    nperseg         -- ühe signaalist võetava akna suurus
    sr              -- sämplimissagedus

    Tagastab:
        None
    """
    # Arvutame spektrogramm faasiga (väljastab faasid vahemikus [-π, π])
    #f, t, Sxx = signal.spectrogram(data, fs=sr, nperseg=nperseg, noverlap=noverlap, mode='phase')
    # Eemaldame logaritmimise, kuna faasipildi puhul seda pole vaja, faaside väärtused
    #Sxx_phase = (Sxx) # Faaside väärtused
    #plot_item.clear()
    # Kuvame faasispektrogrammi

    # Kasuta mode='complex' kompleksarvude saamiseks
    f, t, Sxx_complex = signal.spectrogram(data, fs=sr, nperseg=nperseg, noverlap=noverlap, mode='angle')

    # Muuda faasiväärtusi enne normaliseerimist, et parandada värvide jaotust
    #Sxx_phase_normalized = (Sxx_phase + np.pi) / (2 * np.pi)  # Skaleeri vahemikku [0, 1]
    #Sxx_phase_normalized = np.exp(1j * Sxx_phase)  # Kasuta eksponeeritud kujutist faasi kujutamiseks

    # Tühjendame eelneva graafiku sisua
    plot_item.clear()

    # Kuvame faasispektrogrammi, kasutades spetsiifilist värviskeemi perioodilisuse esitamiseks
    plot_image(plot_item, (Sxx_complex), dt=t[1] - t[0], df=f[1] - f[0], colormap='CET-C7', phase=True)


    # Märgiste lisamine sõltuvalt sellest, kas sämplimissagedus on määratud
    if sr is not None:
        plot_item.setLabel('bottom', "Aeg (s)")
        plot_item.setLabel('left', "Sagedus", units="Hz")
    else:
        plot_item.setLabel('bottom', "Andmepunkti indeks")
        plot_item.setLabel('left', "Sagedus murdosana sämplimiskiirusest")
    # Automaatne ulatuse kohandamine
    plot_item.getViewBox().autoRange()