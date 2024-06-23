#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def analysis(data, extra_params):
    """
    Funktsioon, mis akendab signaali lõigu ning teisendab selle sagedusruumi.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid

    Tagastab:
        Akendatud signaali lõigu sagedusruumi esitus
    """
    # Võtame extra_params'ist akna suuruse, vaikimisi on see 1024.
   # win_size = extra_params.get('win_size', 1024)
    # Loome Hann'i akna, mis on pool-kosinuse kujuline aknafunktsioon.
    # Hann'i akna kasutamine vähendab servamoonutusi Fourier' teisenduses.
    window = np.hanning(len(data))
    
    # Kui sisendsignaali pikkus on väiksem kui akna suurus,
    # pikendame signaali nullidega lõpuni.
    #if len(data) < win_size:
    #    data = np.pad(data, (0, win_size - len(data)), 'constant')
    
    # Rakendame akna andmetele. See samm vähendab lekkeefekti sagedusruumis,
    # mis on oluline, et vältida spektri serval asuvate komponentide moonutusi.
    windowed_data = data * window
    # Viime akendatud andmed sagedusruumi, kasutades reaalarvulist Fourier' teisendust.
    # RFFT on efektiivsem kui FFT reaalarvulistele andmetele,
    # kuna see annab ainult positiivsed sagedused.
    freq_data = np.fft.rfft(windowed_data)
    return freq_data


def synthesis(data, extra_params):
    """
    Funktsioon, mis teisendab signaali lõigu tagasi aegruumi ning akendab selle.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid

    Tagastab:
        Akendatud tulemussignaal aegruumis
    """
    # Võtame extra_params'ist akna suuruse, vaikimisi on see 1024.
   # win_size = extra_params.get('win_size', 1024)
    # Viime sagedusruumi andmed tagasi aegruumi, kasutades reaalarvulist Fourier' pöördteisendust.
    # IRFFT kasutab andmete teisendamiseks ainult positiivseid sagedusi.
    time_data = np.fft.irfft(data)
    
    # Loome uuesti Hann'i akna, mida kasutame akendamiseks.
    window = np.hanning(len(time_data))
    
    # Kui aegruumi teisendatud andmed on lühemad kui akna suurus,
    # pikendame neid nullidega lõpuni.
  #  if len(time_data) < win_size:
   #     time_data = np.pad(time_data, (0, win_size - len(time_data)), 'constant')
    
    # Rakendame akna aegruumi andmetele.
    # See samm on oluline, et vähendada võimalikke artefakte, mis tekivad signaali taastamisel.
    windowed_time_data = time_data * window
    return windowed_time_data


def sanity_check(data, extra_params):
    """
    Signaali lõigu kaupa töötlemise funktsioon, mis ei tee midagi sisendandmetega.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid

    Tagastab:
        Signaali lõigu
    """
    return data


def robotize(data, extra_params):
    """
    Funktsioon, mis sooritab signaali lõigul robotiseerimise efekti.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid

    Tagastab:
        Robotiseeritud signaali lõik sagedusruumis
    """
    # 1. Sagedusruumi teisendamine
    # Kasutame analysis() funktsiooni, et viia heli lõik sagedusruumi. See hõlmab akendamist ja RFFT rakendamist.
    #freq_data = analysis(data, extra_params)
    
    # 2. Magnituudi arvutamine
    # Arvutame sageduskomponentide magnituudid. np.abs() arvutab kompleksarvude absoluutväärtused,
    # mis eemaldab faasi mõju, jättes ainult magnituudi.
    magnitude = np.abs(data)

    # 3. Faaside nullimine
    # Loome nullidest koosneva massiivi, mille kuju vastab freq_data faasidele.
    # np.angle() annab iga kompleksarvu faasi radiaanides, kuid me asendame need nullidega,
    # et saavutada robotiseeritud heliefekt, kus kõik faasid on sünkroniseeritud.

    #zero_phases = np.zeros_like(np.angle(freq_data))

    # 4. Robotiseeritud sagedusandmete loomine
    # Kombineerime magnituudid nullfaasidega, kasutades Euleri valemit.
    # Euleri valem e^(i*phase) kus phase on 0, muutub lihtsalt 1-ks (e^0 = 1), nii et iga kompleksarv
    # on lihtsalt selle magnituud (magnitude*1).

    #robotized_freq_data = magnitude * np.exp(1j * zero_phases)
    
    # 5. Tagastame robotiseeritud sagedusandmed
    # Tulemuseks on kompleksarvuline massiiv, kus kõik elemendid on reaalarvud (magnituudid)
    # ja imaginaarosa on 0, kuna faasid on nullitud.
    return magnitude

def whisperize(data, extra_params):
    """
    Funktsioon, mis sooritab signaali lõigul sosinastamise efekti.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid

    Tagastab:
        Sosinastatud signaali lõik sagedusruumis
    """
    # Viige lõik sagedusruumi kasutades analysis() funktsiooni.
    # See samm hõlmab andmete akendamist ja RFFT kasutamist, et teisendada andmed sagedusruumi.
    #freq_data = analysis(data, extra_params)
    
    # Muudame faasid juhuslikeks väärtusteks
    # Kõigepealt arvutame magnituudid, mis on vajalikud, kuna me soovime säilitada algse heli amplituudi,
    # kuid muuta faasid juhuslikeks.
    magnitude = np.abs(data)
    
    # Genereerime juhuslikud faasid iga sageduskomponendi jaoks.
    # np.random.uniform on kasutatud juhuslike väärtuste genereerimiseks vahemikus [-π, π),
    # mis vastab võimalikele faasiväärtustele.
    random_phase = np.exp(1j * np.random.uniform(-np.pi, np.pi, len(data)))
    
    # Kombineerime magnituudid uute juhuslike faasidega.
    # See samm loob uued kompleksarvud, kus iga komponent koosneb algsest magnituudist
    # ja juhuslikult genereeritud faasist.
    whisperized_freq_data = magnitude * random_phase
    
    # Tagastame sagedusruumi andmed, mis on nüüd "sosinastatud", st magnituudid on säilinud,
    # kuid faasid on asendatud juhuslike väärtustega.
    return whisperized_freq_data


def noise_cancellation(data, extra_params):
    """
    Funktsioon, mis sooritab signaali lõigul müra vähendamise efekti.

    Argumendid:
    data -- signaali lõik
    extra_params -- OverlapAdd klassi isendi lisaparameetrid, muuhulgas R, mis tähistab, kui palju funktsioon müra vähendab

    Tagastab:
        Robotiseeritud signaali lõik sagedusruumis
    """
    # Võtab R väärtuse, mis määrab müra vähendamise määra.
    R = extra_params.get('R', 1)  # Kui R pole määratud, kasutatakse vaikimisi väärtust 1.

    # Arvuta sageduskomponentide magnituudid sagedusruumi andmetest.
    magnitude = np.abs(data)

    # Rakenda Valem 1 magnituudidele.
    # |Xnew| = |X|^2 / (|X| + R)
    # Kus |X| on algne magnituud ja R on positiivne konstant.
    # Suurema magnituudiga komponente korrigeeritakse vähem kui väiksema magnituudiga komponente,
    # aidates seeläbi vähendada müra, eeldusel, et müra on väiksema magnituudiga.
    new_magnitude = magnitude**2 / (magnitude + R)

    # Faasi info säilitamine
    phase = np.angle(data)

    # Taasta sagedusruumi andmed kasutades uusi magnituude ja algseid faase.
    new_freq_data = new_magnitude * np.exp(1j * phase)

    # Tagasta müra vähendatud sagedusruumi andmed.
    return new_freq_data


def predict_phase(dt, freq, prev_phase):
    """
    Funktsioon, mis ennustab kindla sageduskomponendi faasi pärast dt sekundit.

    Argumendid:
    dt -- ajamuut (s)
    freq -- sagedus (Hz)
    prev_phase -- faas enne ajamuutu

    Tagastab:
        Ennustatud faas pärast ajamuutu
    """
    # Arvutan faasi muutuse: delta_phase = dt * freq * 2 * pi
    phase_change = dt * freq * 2 * np.pi

     # Arvutan ennustatud faasi, lisades faasi muutuse eelmisele faasile
    predicted_phase = prev_phase + phase_change

    return predicted_phase




def phase_unwrap(phase, phase_prediction):
    """
    Funktsioon, mis teisendab faasi võimalikult lähedale teisele faasile.

    Argumendid:
    phase -- faas, mida teisendada
    phase_prediction -- faas, mille lähedale tahame teisendada

    Tagastab:
        Ennustatud faas pärast ajamuutu
    """
    # Arvutan faaside erinevus
    diff = phase_prediction - phase
    
    diff = 2 * np.pi * np.round(diff / (2 * np.pi))  # Normalizeerib faasi erinevuse

    unwrapped_phase = phase + diff
    return unwrapped_phase

def real_frequency(phase_unwrapped, prev_phase, dt):
    """
    Arvuta tegelik sagedus kasutades lahtipakitud faasi ja eelmise akna faasi.

    Argumendid:
    phase_unwrapped -- lahtipakitud faas selle akna jaoks (θunwrapped)
    prev_phase -- eelmise akna faas (θprevious)
    dt -- kahe akna vaheline aeg (Δt)

    Tagastab:
    freal -- leitud tegelik sagedus selle sageduskomponendi jaoks
    """
    # Arvutan faaside vahe
    delta_theta_real = phase_unwrapped - prev_phase
    
    # Arvutan tegelik sageduse, normaliseerides faasi muutuse kahe akna vahelise ajaga
    freal = delta_theta_real / (dt * 2 * np.pi)
    
    return freal


prev_window_phases = None # Muutuja eelmise akna faaside hoidmiseks
last_output_phases = None # Muutuja eelmise akna väljundfaaside hoidmiseks

has_printed = False

def pitch_shift(data, extra_params):

    global prev_window_phases
    global has_printed

    sr = extra_params['sr'] # Sämplimissagedus (Hz)
    win_size = extra_params['win_size'] # Akna suurus
    hop_size = extra_params['hop_size'] # Sammu suurus
    pitch_shift_ratio = extra_params['pitch_shift_ratio'] # Helikõrguse muutmise suhe

    delta_dft = sr / win_size # Sageduse eraldusvõime
    #delta_dft = sr / len(data)
    dt = hop_size / sr # Kahe akna vaheline aeg (sekundites)

    # Teisendan andmed sagedusruumi
    magnitudes = np.abs(data)  # Arvutan sageduskomponentide magnituudid
    phases = np.angle(data) # Arvutan sageduskomponentide faasid

    # Algväärtusta prev_window_phases, kui see on None
    if prev_window_phases is None:
        prev_window_phases = phases.copy()

    # Loome väljundi jaoks samasugused massiivid
    new_magnitudes =  np.zeros_like(magnitudes) # Nullidega täidetud massiiv magnituudide jaoks
    new_phases = np.zeros_like(phases) # Nullidega täidetud massiiv faaside jaoks

  # Itereerime üle kõikide sageduskomponentide
    for k in range(len(data)):
        freq_k = k * delta_dft
        predicted_phase = predict_phase(dt, freq_k, prev_window_phases[k])
        new_phases[k] = predicted_phase
            
    # Kombineerime magnituudid ja faasid tagasi
    output_data = magnitudes * np.exp(1j * new_phases)

    # Uuendame eelmise akna faasiinfot käesoleva akna faasiinfoga
    prev_window_phases = phases.copy()

    if not has_printed:
        for k in range(5):
            print(f"Komponendi {k} ennustatud faas: {new_phases[k]:.4f}")
        has_printed = True

    return output_data


prev_window_phases = None # Muutuja eelmise akna faaside hoidmiseks
last_output_phases = None # Muutuja eelmise akna väljundfaaside hoidmiseks
has_printed = False



def pitch_shift_with_unwrap(data, extra_params):

    global prev_window_phases
    global has_printed


    sr = extra_params['sr'] # Sämplimissagedus
    win_size = extra_params['win_size'] # Akna suurus
    hop_size = extra_params['hop_size'] # Sammu suurus
    pitch_shift_ratio = extra_params['pitch_shift_ratio'] # Helikõrguse muutmise suhe

    #delta_dft = sr / win_size # Sageduse eraldusvõime
    delta_dft = sr / win_size
    dt = hop_size / sr # Kahe akna vaheline aeg (sekundites)

    magnitudes = np.abs(data) # Arvutan sageduskomponentide magnituudid
    phases = np.angle(data) # Arvutan sageduskomponentide faasid

    # Algväärtusta prev_window_phases, kui see on None
    if prev_window_phases is None:
        prev_window_phases = phases.copy()

    new_magnitudes = np.zeros_like(magnitudes) # Nullidega täidetud massiiv uute magnituudide jaoks
    new_phases = np.zeros_like(phases) # Nullidega täidetud massiiv uute faaside jaoks

    # Eeldatavad faasid testimiseks
    expected_phases = [0.0, 1.9670, 2.2080, 4.4175, 7.2273]

    for k in range(len(magnitudes)):
        freq_k = k * delta_dft # Arvuta sageduskomponendi k sagedus
        predicted_phase = predict_phase(dt, freq_k, phases[k]) # Ennusta faas
        unwrapped_phase = phase_unwrap(phases[k], predicted_phase) # Lahtipaki faas
        #new_index = int(k * pitch_shift_ratio) # Arvuta uus indeks helikõrguse muutmise suhtes

        #if new_index < len(magnitudes): # Kontrollin, et uus indeks ei ületa massiivi piire
            #new_magnitudes[new_index] = magnitudes[k] # Uuenda magnituud
        #new_phases[new_index] = unwrapped_phase # Uuenda faas

        # Piira printimist esimese viie komponendi ja ühekordse väljundiga
        if not has_printed and k < 5:
            print(f"Komponendi {k} lahtipakitud faas: {unwrapped_phase:.4f} (Oodatud: {expected_phases[k]:.4f})")

    if not has_printed:
        has_printed = True  # Seadista True peale esimest printimist

    output_data = new_magnitudes * np.exp(1j * new_phases)

    return output_data


def pitch_shift_with_unwrap_real_frequency(data, extra_params):

    global prev_window_phases
    global has_printed

    sr = extra_params['sr'] # Sämplimissagedus
    win_size = extra_params['win_size']  # Akna suurus
    hop_size = extra_params['hop_size'] # Sammu suurus
    pitch_shift_ratio = extra_params['pitch_shift_ratio'] # Helikõrguse muutmise suhe
    dt = hop_size / sr  # Kahe akna vaheline aeg (sekundites)

    magnitudes = np.abs(data) # Arvutan sageduskomponentide magnituudid
    phases = np.angle(data) # Arvutan sageduskomponentide faasid

    # Algväärtusta prev_window_phases, kui see ei ole juba extra_params sõnastikus
    if 'prev_window_phases' not in extra_params:
        extra_params['prev_window_phases'] = phases.copy()

    new_magnitudes = np.zeros_like(magnitudes) # Nullidega täidetud massiiv uute magnituudide jaoks
    new_phases = np.zeros_like(phases) # Nullidega täidetud massiiv uute faaside jaoks
    real_frequencies = [] # List tegelike sageduste hoidmiseks

    for k in range(len(data)):
        freq_k = k * sr / win_size  # Arvuta sageduskomponendi k sagedus
        predicted_phase = predict_phase(dt, freq_k, phases[k]) # Ennusta faas
        unwrapped_phase = phase_unwrap(phases[k], predicted_phase) # Lahtipaki faas
        real_frequency_value = real_frequency(unwrapped_phase, extra_params['prev_window_phases'][k], dt) # Arvuta tegelik sagedus
        #new_index = int(k * pitch_shift_ratio) # Arvuta uus indeks helikõrguse muutmise suhtes

        #if new_index < len(magnitudes):
            #new_magnitudes[new_index] = magnitudes[k] # Uuenda magnituud
        #new_phases[new_index] = unwrapped_phase # Uuenda faas
        #real_frequencies.append(real_frequency_value) # Lisa tegelik sagedus listi

        if not has_printed and k < 5:
            print(f"Component {k}: Real frequency = {real_frequency_value:.4f} Hz")

    if not has_printed:
        has_printed = True

    prev_window_phases = phases.copy()
    output_data = new_magnitudes * np.exp(1j * new_phases)
    return output_data, real_frequencies



prev_window_phases = None
last_output_phases = None
has_printed = False

def pitch_shift_6_5(data, extra_params):
    global prev_window_phases, last_output_phases, has_printed

    # Võta kasutusele sagedus, akna suurus ja sammu suurus extra_params sõnastikust
    sr = extra_params['sr']  # Sämplimissagedus Hz
    win_size = extra_params['win_size']  # Akna suurus
    hop_size = extra_params['hop_size']  # Sammu suurus
    pitch_shift_ratio = extra_params.get('pitch_shift_ratio', 1.2)  # Helikõrguse muutmise suhe
    dt = hop_size / sr  # Aeg kahe akna vahel sekundites

    magnitudes = np.abs(data)  # Arvuta sageduskomponentide magnituudid
    phases = np.angle(data)  # Arvuta sageduskomponentide faasid
    delta_dft = sr / win_size  # Sageduse eraldusvõime

    # Algväärtusta prev_window_phases ja last_output_phases, kui need ei ole juba initsialiseeritud
    if prev_window_phases is None:
        prev_window_phases = np.copy(phases)
    if last_output_phases is None:
        last_output_phases = np.copy(phases)

    # Loo uued massiivid muudetud magnituudide ja faaside jaoks
    new_magnitudes = np.zeros_like(magnitudes)
    new_phases = np.zeros_like(phases)
    real_frequencies = []

    for k in range(len(data)):
        freq_k = k * sr / win_size  # Arvuta sageduskomponendi k sagedus
        predicted_phase = predict_phase(dt, freq_k, phases[k]) # Ennusta faas
        unwrapped_phase = phase_unwrap(phases[k], predicted_phase) # Lahtipaki faas
        real_frequency_value = real_frequency(unwrapped_phase, prev_window_phases[k], dt) # Arvuta tegelik sagedus
        
        freal_shifted = real_frequency_value * pitch_shift_ratio  # Skaleeritud sagedus

        # Arvutan väljundi indeks
        foutput_i = round(freal_shifted / delta_dft)  # Calculate output index

        # Kontrolli, kas indeks jääb massiivi piiridesse
        if 0 < foutput_i < len(data):
            new_magnitudes[foutput_i] += magnitudes[k] # Liida olemasolevale magnituudile
            # Võtan eelmise akna väljundfaasi, kui indeks on olemas, muidu kasutan praegust faasi
            theta_synth_prev = last_output_phases[foutput_i] # if foutput_i < len(last_output_phases) else phases[k]
            # Arvutan uue faasi, lisades skaleeritud sageduse põhjustatud faasi muutuse
            theta_synth = theta_synth_prev + freal_shifted * dt * 2 * np.pi
            new_phases[foutput_i] = theta_synth


        # Prindi väljundid ainult esimesel käivitamisel ja piira väljundit esimese viie komponendiga
        if not has_printed and k < 5:
            print(f"Component {k}: New frequency = {freal_shifted:.4f} Hz, New index = {foutput_i}, New phase = {new_phases[foutput_i]:.4f}")

    if not has_printed:
        has_printed = True  # Märgi, et väljundid on juba prinditud

    # Uuenda faasi massiive järgmise akna jaoks
    prev_window_phases = phases
    last_output_phases = new_phases

    # Kombineeri uued magnituudid ja faasid komplekssignaaliks
    output_data = new_magnitudes * np.exp(1j * new_phases)
    return output_data
