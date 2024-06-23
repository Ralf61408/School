#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal


# Ülesandes 1 implementeeritavad funktsioonid:

def create_lowpass(cutoff_freq: float, transition_bw: float, windowed: bool=True) -> np.array:
    """
    Funktsioon, mis tekitab madalpääsfiltri kerneli.

    Argumendid:
    cutoff_freq   -- mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    transition_bw -- siirdeala laius murdosana sämplimissagedusest vahemikus (0, 1)
    windowed      -- määrab kas filtrile rakendatakse aknafunktsiooni.

    Tagastab:
        loodud madalpääsfiltri kernel
    """
    # Arvutame mahalõikesageduse
    
    # Arvutame filtri akna pikkuse M
    M = int(4 / transition_bw)
    if M % 2 == 0:
        M += 1

    # Loome kerneli
    kernel = np.zeros(M)
    for i in range(M):
        if i == (M - 1) // 2:
            kernel[i] = 2 * np.pi * cutoff_freq  # Keskpunkti väärtus
        else:
            kernel[i] = np.sin(2 * np.pi * cutoff_freq * (i - (M - 1) / 2)) / (i - (M - 1) / 2)

    # Rakendame aknafunktsiooni
    if windowed:
        black = create_blackman_window(M)
        kernel *= black

    kernel2 = kernel/sum(kernel)

    return kernel2


def transform_filter_kernel(filter_time: np.array) -> np.array:
    """
    Funktsioon, mis teisendab filtri aegruumist sagedusruumi.

    Argumendid:
    filter_time -- filter aegruumis.

    Tagastab:
       filter sagedusruumis
    """
    # Leian filter aegruumis DFT abil
    filter_freq = np.fft.rfft(filter_time)

    # Tagastan filteri aegruumis
    return filter_freq


def create_blackman_window(window_size: int) -> np.array:
    """
    Funktsioon, mis loob soovitud suurusega Blackman'i akna.

    Argumendid:
    window_size -- filtri akna pikkus

    Tagastab:
        loodud Blackman'i aken
    """
    #a = np.array([0.42, 0.5, 0.08])
    n = np.arange(window_size)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (window_size)) + 0.08 * np.cos(4 * np.pi * n / (window_size))


# Ülesandes 3 implementeeritav funktsioon:

def apply_filter(filter: np.array, data: np.array) -> np.array:
    """
    Funktsioon, mis rakendab filtri kernelit sisendandmetele.

    Argumendid:
    filter -- filtri kernel
    data   -- sisendandmed

    Tagastab:
        filtreeritud andmed
    """
    filtered_data = scipy.signal.convolve(data, filter)

    return filtered_data


# Ülesandes 4 implementeeritav funktsioon:

def create_highpass_spectral_inversion(cutoff_freq: float, transition_bw: float) -> np.array:
    """
    Funktsioon, mis tekitab kõrgpääsfiltri kerneli kasutades abifunktsioonina madalpääsfiltri loomist.

    Argumendid:
    cutoff_freq   -- mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    transition_bw -- siirdeala laius murdosana sämplimissagedusest vahemikus (0, 1)

    Tagastab:
        loodud kõrgpääsfiltri kernel
    """
    # loome normaliseeritud madalpääsfiltri
    lowpass_kernel = create_lowpass(cutoff_freq, transition_bw)

    # Korrutame iga väärtuse -1
    highpass_kernel = -1 * lowpass_kernel

    # Lisame keskpunktis olevale väärusele 1
    highpass_kernel[(len(highpass_kernel) - 1) // 2] += 1

    return highpass_kernel

# Ülesandes 6 implementeeritav funktsioon:

def create_bandpass(low_cutoff_freq: float, high_cutoff_freq: float, transition_bw: float) -> np.array:
    """
    Funktsioon, mis tekitab ribapääsfiltri kerneli kasutades abifunktsioonidena madalpääsfiltri ja kõrgpääsfiltri loomist.

    Argumendid:
    low_cutoff_freq  -- madalam mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    high_cutoff_freq -- kõrgem mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    transition_bw    -- siirdeala laius murdosana sämplimissagedusest vahemikus (0, 1)

    Tagastab:
        loodud ribapääsfiltri kernel
    """
    # Loome madalpääsfiltri kerneli
    lowpass_kernel = create_lowpass(high_cutoff_freq, transition_bw)
    
    # Loome kõrgpääsfiltri kerneli
    highpass_kernel = create_highpass_spectral_inversion(low_cutoff_freq, transition_bw)
    
    # Konvoleerime kernelid ajas
    bandpass_kernel = np.convolve(lowpass_kernel, highpass_kernel)
    
    # Tagastame ribapääsfiltri kerneli
    return bandpass_kernel

# Ülesandes 8 implementeeritav funktsioon:

def create_bandstop(low_cutoff_freq: float, high_cutoff_freq: float, transition_bw: float) -> np.array:
    # Funktsioon peab looma sobivad madal- ja kõrgpääsfiltrid ja kombineerima need üheks ribatõkkefiltriks
    """
    Funktsioon, mis tekitab ribatõkkefiltri kerneli kasutades abifunktsioonidena madalpääsfiltri ja kõrgpääsfiltri loomist.

    Argumendid:
    low_cutoff_freq  -- madalam mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    high_cutoff_freq -- kõrgem mahalõikesagedus murdosana sämplimissagedusest vahemikus (0, 0.5)
    transition_bw    -- siirdeala laius murdosana sämplimissagedusest vahemikus (0, 1)

    Tagastab:
        loodud ribatõkkefiltri kernel
    """
    # Arvutame sobiva akna pikkuse M
    #M = int(4 / transition_bw)
    # if M % 2 == 0:
    #     M += 1
    
    # Arvutame läbilaskvuspiirid
   # stopband_low = low_cutoff_freq - transition_bw/2
   # stopband_high = high_cutoff_freq + transition_bw/2

    # Loome madalpääsfiltri kerneli
    lowpass_kernel = create_lowpass(low_cutoff_freq, transition_bw)
    
    # Loome kõrgepääsfiltri kerneli ja rakendame spektri inversiooni
    highpass_kernel = create_highpass_spectral_inversion(high_cutoff_freq, transition_bw)
    
    # Kombineerime madal- ja kõrgpääsfiltri kernelid ribatõkkefiltri kerneliks
    bandstop_kernel = lowpass_kernel + highpass_kernel

    return bandstop_kernel

def main():
    print("Seda faili pole vaja jooksutada!")

if __name__ == '__main__':
    main()
