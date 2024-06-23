#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from scipy.io.wavfile import read, write
import scipy.io.wavfile as wav
from dst.fourier.overlapadd.OverlapAdd import OverlapAdd
from dst.fourier.overlapadd.vocoder_dependencies import analysis, noise_cancellation, pitch_shift, robotize, sanity_check, synthesis, whisperize, predict_phase, pitch_shift_with_unwrap, pitch_shift_with_unwrap_real_frequency, pitch_shift_6_5
from dst.visual.plot_filters import plot_spectrogram, plot_phase_spectrogram


SCRIPT_PATH = os.path.dirname(__file__)
prev_window_phases = None
has_printed = False

def normalise(data):
    """
    Funktsioon, mis normaliseerib helifaili vahemikku [-1, 1], säilitades nulli ümber tsentreeritust.

    Argumendid:
        data             -- np.array, sisendsignaal

    Tagastab:
        norm_data        -- np.array, normaliseeritud sisendsignaal
    """
    # Maksimaalse absoluutväärtuse leidmine
    max_val = np.max(np.abs(data))
    # Normaliseerimine vahemikku [-1, 1]
    norm_data = data / max_val  # Jagab iga massiivi elemendi maksimaalse absoluutväärtusega, normaliseerides andmed
    return norm_data

def read_audio(filename):
    # TODO: Lugege sisse helifail, kasutades scipy.io.wavfile.read funktsiooni
    #sr, data = 8000, np.zeros(8000)
    # TODO: Kui tegemist on stereofailiga, siis tuleb see teisendada monoks
    # TODO: Normaliseerige tulemus

    # Helifaili sisselugemine; 'read' funktsioon tagastab helifaili samplimissageduse ja andmed
    sr, data = wav.read(filename)
    
    # Kontrollib, kas helifail on mitmekanaliline (näiteks stereo)
    # Kui 'data' on mitmemõõtmeline (data.shape > 1), siis on helifailis rohkem kui üks kanal
    if len(data.shape) > 1:
        # Arvutab kõikide kanalite keskmise, et luua üks kanal
        data = np.mean(data, axis=1)

    # Kasutab funktsiooni normalise() andmete normaliseerimiseks vahemikku [-1, 1]
    norm_data = normalise(data)

    return sr, norm_data


def display_spectrogram(input_data, output_data=None, win_size=1024, hop_size=256, sr=None, title="yl2"):
    noverlap = win_size - hop_size

    # Loo graafiku aken
    win = pg.GraphicsLayoutWidget(show=True, title=title)

    # Kuvame sisendi magnituudide spektrogrammi
    input_mag_plot = win.addPlot(title="Sisend, magnituudid")
    plot_spectrogram(input_mag_plot, input_data, noverlap=noverlap, nperseg=win_size, sr=sr)

    # Järgmine rida
    win.nextRow()

    # Kuvame sisendi faaside spektrogrammi
    input_phase_plot = win.addPlot(title="Sisend, faasid")
    plot_phase_spectrogram(input_phase_plot, input_data, noverlap=noverlap, nperseg=win_size, sr=sr)

    if output_data is not None:
        # Järgmine rida
        win.nextRow()

        # Kuvame väljundi magnituudide spektrogrammi
        output_mag_plot = win.addPlot(title="Väljund, magnituudid")
        plot_spectrogram(output_mag_plot, output_data, noverlap=noverlap, nperseg=win_size, sr=sr)

        # Järgmine rida
        win.nextRow()

        # Kuvame väljundi faaside spektrogrammi
        output_phase_plot = win.addPlot(title="Väljund, faasid")
        plot_phase_spectrogram(output_phase_plot, output_data, noverlap=noverlap, nperseg=win_size, sr=sr)

    # Kuvame akna
    QtWidgets.QApplication.instance().exec_()
    

def yl1():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_quiet.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_yl1_output.wav")
    sr, data = read_audio(file_path)
    write(out_path, sr, (data * 32767).astype(np.int16))
    print(f"Helifail '{file_path}' on edukalt normaliseeritud ja salvestatud faili '{out_path}'.")
    # Korrutamine väärtusega 32767 skaleerib normaliseeritud helifaili andmed 16-bitise PCM (Pulse Code Modulation) helifaili
    # astype(np.int16) teisendab skaleeritud andmed 16-bitisteks täisarvudeks, mis on standardne formaat PCM helifailide jaoks WAV-failides.

def yl2():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_im_a_robot.wav")
    sr, data = read_audio(file_path)
    win_size = 1024
    hop_size = 256

    display_spectrogram(data, None, win_size, hop_size, sr, "yl2_input")
    display_spectrogram(data, data, win_size, hop_size, sr, "yl2_input_output")


def yl3():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_im_a_robot.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_yl3_output.wav")
    sr, data = read_audio(file_path)
    win_size = 1024
    hop_size = 256
    overlap_add = OverlapAdd(win_size, hop_size, data.shape[0], analysis, sanity_check, synthesis)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, "yl3")


def yl4():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_im_a_robot.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_robotized_output_1024_256.wav")
    sr, data = read_audio(file_path)
    
    # Erinevate akende ja sammude katsetamine
    win_size = 1024
    hop_size = 256
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, robotize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_robotize_{win_size}_{hop_size}")

    # Proovime erinevaid akende suurusi ja samme
    win_size = 2050
    hop_size = 256
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, robotize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_robotized_output_512_128.wav")
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_robotize_{win_size}_{hop_size}")

    win_size = 32
    hop_size = 10
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, robotize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_robotized_output_2048_512.wav")
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_robotize_{win_size}_{hop_size}")


def yl4_whisperize():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_im_a_robot.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_whisperized_output_1024_232.wav")
    sr, data = read_audio(file_path)
    
    # Erinevate akende ja sammude katsetamine
    win_size = 1024
    hop_size = 32
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, whisperize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_whisperize_{win_size}_{hop_size}")

    # Proovime erinevaid akende suurusi ja samme
    win_size = 1024
    hop_size = 2000
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, whisperize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_whisperized_output_1024_2000.wav")
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_whisperize_{win_size}_{hop_size}")

    win_size = 1024
    hop_size = 4000
    
    extra_params = {'win_size': win_size}
    
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, whisperize, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_whisperized_output_1024_4000.wav")
    write(out_path, sr, output)
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl4_whisperize_{win_size}_{hop_size}")


def yl5():
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_noisy_talk.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_noise_reduced_output.wav")
    sr, data = read_audio(file_path)

    # Määrame akna ja hüppe suurused
    win_size = 1024
    hop_size = 256

    # Määrame R väärtuse
    R = 50  # Seda väärtust võib muuta ja katsetada, nii tuli väga hea, et sahisemist jne enam ei olnud. Proovisin ka 5000 väärtusega, aga vist hakkas veidike tummisemaks minema, muidu oli korras.

    extra_params = {'win_size': win_size, 'R': R}

    # Loome OverlapAdd klassi instantsi
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, noise_cancellation, synthesis, extra_params)
    output = normalise(overlap_add.run(data))

    # Kirjutame väljundfaili
    write(out_path, sr, output)

    # Kuvame spektrogrammid
    display_spectrogram(data, output, win_size, hop_size, sr, f"yl5_noise_reduction_R_{R}")


def yl6():
    
   # Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift() funktsiooni.
    
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    sr, data = read_audio(file_path)

    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift, synthesis, extra_params)
    output = (overlap_add.run(data))

    # Tagasta väljund
    return output


def yl6_unwrap():
    """
    Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap() funktsiooni.
    Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    """
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_with_unwrap, synthesis, extra_params)
    output = (overlap_add.run(data))


    # Tagasta töödeldud andmed edasiseks analüüsiks või testimiseks
    return output


def yl6_unwrap_real_frequency():
    """
    Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    """
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_with_unwrap_real_frequency, synthesis, extra_params)
    output = (overlap_add.run(data))


    # Tagasta töödeldud andmed edasiseks analüüsiks või testimiseks
    return output


def yl6_unwrap_6_5():
    """
    Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    """
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = (overlap_add.run(data))


    # Tagasta töödeldud andmed edasiseks analüüsiks või testimiseks
    return output

def yl6_unwrap_6_6():
    """
    Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    """
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland_1024_256.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)

    # Kuvame spektrogrammid
    display_spectrogram(data, output, win_size, hop_size, sr)

    # Proovime erinevaid akende suurusi ja samme
    
    """
   
    #Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    #Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland_1024_800.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 800
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)

    # Proovime erinevaid akende suurusi ja samme

    
    #Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    #Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland_4000_256.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 4000
    hop_size = 256
    pitch_shift_ratio = 1.2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)

    
    
   # Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
   # Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland_1024_256_0.6.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 0.6
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)


    
    #Funktsioon, mis loeb helifaili ja rakendab sellele pitch_shift_with_unwrap_real_frequency() funktsiooni.
    #Samuti logib funktsioon välja kõik faasid ja võrdleb neid ootuspäraste faasidega.
    
    file_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland.wav")
    out_path = os.path.join(SCRIPT_PATH, "andmed/audio/p10_vocal_greenland_1024_256_2.0.wav")
    sr, data = read_audio(file_path)

    # Seadista parameetrid
    win_size = 1024
    hop_size = 256
    pitch_shift_ratio = 2
    extra_params = {'sr': sr, 'win_size': win_size, 'hop_size': hop_size, 'pitch_shift_ratio': pitch_shift_ratio}
    overlap_add = OverlapAdd(win_size, hop_size, len(data), analysis, pitch_shift_6_5, synthesis, extra_params)
    output = normalise(overlap_add.run(data))
    write(out_path, sr, output)
    """

        

def main():
    # yl1()
    # yl2()
    # yl3()
    # yl4()
    # yl4_whisperize()
    # yl5()
    # yl6()
    # yl6_unwrap()
    #yl6_unwrap_real_frequency()
    #yl6_unwrap_6_5()
    yl6_unwrap_6_6()
    
    


if __name__ == "__main__":
    main()
