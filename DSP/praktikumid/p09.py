#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
# Piltide kaustatee
images_path = os.path.join(os.path.dirname(__file__), "andmed/images")
from abi.TrackbarUpdateHandler import TrackbarUpdateHandler





def yl1():
    # Loeb sisse pildi kasutades kaustateed
    goal_img = cv2.imread(os.path.join(images_path, "p09_yl_1_goal.png"))

    if type(goal_img) == type(None):
        print("Jooksuta piltide genereerimiseks koodi failis abi/p09_create_goal_images.py")
        return
    
    # Defineerin väljundi pildi suuruse
    IMG_SIZE = (256, 256)

    # Loo tühi sagedusruum
    freq_space = np.zeros(IMG_SIZE, dtype=np.complex64)

    # Lisan sobivad sageduskomponendid
    freq_space[0, 6] = 1  # katsetamise või analüüsi põhjal

    # Teisenda sagedusruumist koordinaatruumi
    signal = np.real(np.fft.ifft2(freq_space))

    # Normaliseeri signaal vahemikku [0, 255]
    img_back_norm = ((signal - np.min(signal)) * 255 / (np.max(signal) - np.min(signal))).astype(np.uint8)

    cv2.imshow("Pilt", img_back_norm)
    # TODO: Implementeerida siin sagedusruumis pildi konstrueerimine

    while cv2.getWindowProperty('Pilt', cv2.WND_PROP_VISIBLE) >= 1:
        if (cv2.waitKey(10) & 0xFF) == ord("q"):
            break
    cv2.destroyAllWindows()

#
def yl2():
    # Defineerime output pildi suuruse
    IMG_SIZE = (256, 256)

    # Loo tühi sagedusruum
    freq_space = np.zeros(IMG_SIZE, dtype=np.complex64)

    # Anname väärtuse kindlale sageduse komponendile
    freq_space[9, 0] = 1  # Horisontaalne signaal

    # Määra faasinihe
    phase_shift = 270  # Faasinihe 270 kraadi
    freq_space *= np.exp(1j * np.deg2rad(phase_shift))

    # Teeme ifft2-te
    signal = np.real(np.fft.ifft2(freq_space))

    # Normaliseerime signaali vahemikku [0, 255]
    img_back_norm = ((signal - np.min(signal)) * 255 / (np.max(signal) - np.min(signal))).astype(np.uint8)

    # Muudame jooned roheliseks (ainult G kanal aktiivne)
    img_back_norm = np.dstack((np.zeros_like(img_back_norm), img_back_norm, np.zeros_like(img_back_norm)))

    # Kuvame signaali
    cv2.imshow("Faasinihkega signaal", img_back_norm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def yl2_2():
    IMG_SIZE = (256, 256)

    # Loo tühjad sagedusruumid iga värvikanali jaoks
    freq_space_R = np.zeros(IMG_SIZE, dtype=np.complex64)
    freq_space_G = np.zeros(IMG_SIZE, dtype=np.complex64)
    freq_space_B = np.zeros(IMG_SIZE, dtype=np.complex64)

    # Anname väärtuse kindlatele sageduse komponentidele
    freq_space_B[2, 2] = 1  # Sinine, horisontaalne
    freq_space_G[8, 0] = 1   # Roheline, diagonaalne
    freq_space_R[0, 4] = 1   # punane, vertikaalne

    # Määran faasinihke sisnise kanali jaoks
    # Määran faasinihke
    #phase_shift muutuja väärtuseks on antud 270, mis tähendab, et faasinihe on 270 kraadi
    phase_shift = 270
     #Seejärel korrutatakse sagedusruum freq_space kujutise kompleksarvulisest esitusest koostatud maatriksiga, mis saadakse np.exp(1j * np.deg2rad(phase_shift)) funktsiooniga. 
    # np.exp funktsioon tagastab kompleksarvu e-massiivi astmes, kus massiivi argumendiks on radiaanides väljendatud faasinurk. 
    # 1j on kompleksarv, mille reaalarvuline osa on 0 ja imaginaarvuline osa on 1, ning np.deg2rad funktsioon teisendab faasinihke kraadid radiaanideks.
    freq_space_B *= np.exp(1j * np.deg2rad(phase_shift))
    #https://blog.seispider.top/post/2018-07-29-phase-shift/

    # Teeme ifft2-te iga kanali jaoks
    signal_R = np.real(np.fft.ifft2(freq_space_R))
    signal_G = np.real(np.fft.ifft2(freq_space_G))
    signal_B = np.real(np.fft.ifft2(freq_space_B))

    # Normaliseerime signaalid vahemikku [0, 255]
    img_R = ((signal_R - np.min(signal_R)) * 255 / (np.max(signal_R) - np.min(signal_R))).astype(np.uint8)
    img_G = ((signal_G - np.min(signal_G)) * 255 / (np.max(signal_G) - np.min(signal_G))).astype(np.uint8)
    img_B = ((signal_B - np.min(signal_B)) * 255 / (np.max(signal_B) - np.min(signal_B))).astype(np.uint8)

    # Kombineeri kolm värvikanalit
    img_back_norm = np.dstack([img_B, img_G, img_R])

    # Kuvame signaali
    cv2.imshow("Kombineeritud signaal", img_back_norm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def yl2_3():
    IMG_SIZE = (1000, 1000)  # Suurendame pildi suurust, et paremini mõjusid näha

    # Loo tühi sagedusruum
    freq_space = np.zeros(IMG_SIZE, dtype=np.complex64)

    # Defineerime sageduskomponentide arvu
    num_components = 37  # Kasutame 40 komponenti ruutsignaali lähendamiseks

    # Loopime läbi iga sageduskomponendi jaoks
    for i in range(num_components):
        #print("jou", i)
        a = 2 * i + 1 # kasutame ainult paarisarvulisi harmoonikuid sest ruutsignaal
        # Loob ajutise maatriksi, mis esindab ühte sageduskomponenti. See on sama suurusega kui freq_space.
        component = np.zeros(IMG_SIZE, dtype=np.complex64)
        #Määrab ühe kindla elemendi component maatriksis, mis vastab a-ndale harmoonikule. 
        #See element määratakse Fourier'i seeria kordajaga, mis on ruutsignaali jaoks 4/(πa). 
        component[13*a, 0] = 4/(np.pi*a) *1j
        #component *= (np.pi) # Faasinihe rakendab faasinihet 90 kraadi.
        #akendab faasinihet radiani igale komponendile, korrutades iga elemendi maatriksis imaginaarühikuga j. 
        #See on vajalik signaali õige faasinihke saavutamiseks.
    
        # Lisame sageduskomponendi sagedusruumi
        freq_space += component

    # Teeme ifft2-te
    signal = np.real(np.fft.ifft2(freq_space))



    # Normaliseerime signaali vahemikku [0, 255]
    img_back_norm = ((signal - np.min(signal)) * 255 / (np.max(signal) - np.min(signal)))
    img_back_norm = img_back_norm.astype(np.uint8)
    #img_back_norm_stack = np.vstack((img_back_norm, img_back_norm, img_back_norm))

    # Kuvame signaali
    cv2.imshow("Signal", img_back_norm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def yl3():
    """
    Funktsioon, mis võtab sisendiks vabalt valitud koordinaatruumis oleva ühe kanaliga pildi ja tagastab selle pildi esituse
    sagedusruumis. Tagastatud sagedusruum on nihutatud nii, et null-sageduslik komponent oleks kujutise keskel ja on 
    logaritmilises skaalas.
    
    :param image_path: ühe kanaliga pildi asukoht
    :return: logaritmilises skaalas nihutatud sagedusruum
    """
    # Loeme pildi sisse 1-kanalilise halskaala pildina
    cat_img = cv2.imread(os.path.join(images_path, "cat.png"), cv2.IMREAD_GRAYSCALE)
    if cat_img is None:
        raise ValueError("Pilti ei suudetud laadida. Kontrollige failiteed ja faili olemasolu.")
    
    # Rakendame Fourier teisendust pildi 2D signaalile
    f = np.fft.fft2(cat_img)
    
    # Nihutame null-sagedusliku komponendi kujutise keskele
    f_shift = np.fft.fftshift(f)
    
    # Võtame sageduskomponentide magnituudid
    magnitude_spectrum = np.abs(f_shift)
    
    # Logaritmime sageduskomponendid, arvestades null-sagedusliku komponendi paiknemist keskel
    magnitude_spectrum = np.log(magnitude_spectrum)
    
    # Normaliseerime sageduskomponendid
    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Kuvame sagedusruumi kujutise
    cv2.imshow("Frequency Spectrum", magnitude_spectrum)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass


def yl4():
    # Lae pilt
    img = cv2.imread(os.path.join(images_path, "p09_yl_4_noisy_cat.png"), cv2.IMREAD_GRAYSCALE)
    
    # Kuva algne pilt
    cv2.imshow('Alguparane Pilt', img)

    # Teisenda pilt sagedusruumi
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift)+1)  # Lisame 1, et vältida log0

    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)


    # Kuva sagedusruumi enne filtreerimist
    cv2.imshow('Sagedusruum enne filtreerimist', magnitude_spectrum.astype(np.uint8))

    # Nullime müraga seotud sageduskomponendid
    # Täpsed indeksid tuleks kindlaks määrata pildi visualiseerimisel või eelanalüüsil
    #fshift[40, 12] = 0
    #fshift[204, 354] = 0
    #fshift[103, 170] = 0
    #fshift[141, 196] = 0
    fshift[135, 141] = 0
    fshift[109, 109] = 0
    fshift[109, 225] = 0

    # Kuva filtreeritud sagedusruum
    filtri_magnitude_spectrum = np.log(np.abs(fshift)+1)
    filtri_magnitude_spectrum = cv2.normalize(filtri_magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow('Filtritud sagedusruum', filtri_magnitude_spectrum.astype(np.uint8))

    # Taastame pildi koordinaatruumis
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)

    # Normaliseeri taastatud pilt kuvamiseks
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Kuva lõplik tulemus
    cv2.imshow('Muravaba kujutis', img_back)
    cv2.waitKey()
    cv2.destroyAllWindows()


""" ülesanne 5 """




def create_filter(magnitude_spectrum, threshold):

    # Kasutab cv2.threshold() funktsiooni, et nullida kõik maski elemendid, mille vastavad magnitude_spectrum väärtused ületavad määratud läve
    _, mask = cv2.threshold(magnitude_spectrum, threshold, 1, cv2.THRESH_BINARY_INV)

    # Loob keskel ringikujulise ala, kus sageduskomponendid jäävad puutumata
    # Võtab magnitude_spectrum ridade ja veergude arvu ja määrab need muutujatele rows ja cols.
    rows, cols = magnitude_spectrum.shape
    # Arvutab magnitude_spectrum keskpunkti koordinaadid (rida ja veerg).
    center_row, center_col = rows // 2, cols // 2
    radius = 6
    # võrguindeksid y ja x, mis vastavad ridadele ja veergudele.
    y, x = np.ogrid[:rows, :cols]
    # Arvutab maski keskse ringikujulise ala loogilise massiivina
    central_area = (x - center_col)**2 + (y - center_row)**2 <= radius**2
    mask[central_area] = 1
    return mask

def apply_filter(fshift, mask):
    # Rakendab maski sagedusruumi andmetele
    fshift_filtered = fshift * mask
    return fshift_filtered

def to_image_space(fshift):
    # Teisendab sagedusruumi andmed tagasi pildiruumi
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img_back

def display_images(filtered_spectrum, filtered_image):
    # Kuva filtritud sagedusruumi ja pildi
    filtered_magnitude_spectrum = np.log(np.abs(filtered_spectrum) + 1)
    filtered_magnitude_spectrum = cv2.normalize(filtered_magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("Filtritud sagedusruum", filtered_magnitude_spectrum)
    cv2.imshow("Filtritud pilt", filtered_image)

def on_trackbar(threshold, img, update_handler):
    # Teisenda pilt sagedusruumi
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    # Loo filter vastavalt lävendile
    mask = create_filter(magnitude_spectrum, threshold)

    # Rakenda filter sagedusruumis
    fshift_filtered = apply_filter(fshift, mask)

    # Teisenda filtreeritud sagedusruum tagasi pildiruumi
    img_filtered = to_image_space(fshift_filtered)

    # Kuva filtritud sagedusruumi ja pildi
    display_images(fshift_filtered, img_filtered)
    
def yl5():
    img_path = 'andmed/images/p09_yl_5_very_noisy_cat.png'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("Ei leitud pilti aadressil: {}".format(img_path))
    
    # Loo aknad sagedusruumi ja filtritud pildi kuvamiseks
    win_name_freq = "Filtritud sagedusruum"
    win_name_img = "Filtritud pilt"
    cv2.namedWindow(win_name_freq)
    cv2.namedWindow(win_name_img)

    threshold = 12
    trackbars_data = {"Lävend": {"cur_value": threshold, "max_value": 255}}
    update_handler = TrackbarUpdateHandler(trackbars_data=trackbars_data, window_name=win_name_freq, response_latency=1)

    # Funktsioon, mida käivitatakse, kui liuguri väärtus muutub
    def trackbar_callback(x):
        threshold = trackbars_data["Lävend"]["cur_value"]
        on_trackbar(threshold, img, update_handler)

    # Loome liugurid ja määrame nende algväärtused ning maksimaalsed väärtused
    for tb_name, tb_params in trackbars_data.items():
        cv2.createTrackbar(tb_name, win_name_freq, tb_params["cur_value"], tb_params["max_value"], trackbar_callback)

    # Rakendame algse lävendi ja kuvame esialgse pildi
    on_trackbar(threshold, img, update_handler)

    # Peatsüklis uuendame pilti vastavalt vajadusele
    while True:
        if update_handler.update_allowed():
            on_trackbar(trackbars_data["Lävend"]["cur_value"], img, update_handler)
        # Kui vajutatakse Q või aken suletakse, lõpetame tsükli
        if (cv2.waitKey(1) & 0xFF) == ord('q') or cv2.getWindowProperty(win_name_freq, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()






""" Ülesanne 6. """





def create_filter_yl6(magnitude_spectrum, threshold, radius):
    # Kasutab cv2.threshold() funktsiooni, et nullida kõik maski elemendid, mille vastavad magnitude_spectrum väärtused ületavad määratud läve
    _, mask = cv2.threshold(magnitude_spectrum, threshold, 1, cv2.THRESH_BINARY_INV)

    rows, cols = magnitude_spectrum.shape
    center_row, center_col = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    central_area = (x - center_col)**2 + (y - center_row)**2 <= radius**2
    mask[central_area] = 1
    return mask

def apply_filter_yl6(fshift, mask):
    fshift_filtered = fshift * mask
    return fshift_filtered

def to_image_space_yl6(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img_back

def display_images_yl6(filtered_spectrum, filtered_image):
    filtered_magnitude_spectrum = np.log(np.abs(filtered_spectrum) + 1)
    filtered_magnitude_spectrum = cv2.normalize(filtered_magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("Filtritud sagedusruum", filtered_magnitude_spectrum)
    cv2.imshow("Filtritud pilt", filtered_image)

def on_trackbar_yl6(threshold, radius, img, update_handler):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    mask = create_filter_yl6(magnitude_spectrum, threshold, radius)
    fshift_filtered = apply_filter_yl6(fshift, mask)
    img_filtered = to_image_space_yl6(fshift_filtered)
    display_images_yl6(fshift_filtered, img_filtered)

def yl6():
    img_path = 'andmed/images/p09_yl_6_noisy_plant.jpg'  
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Ei leitud pilti aadressil: {img_path}")
    
    win_name_freq = "Filtritud sagedusruum"
    win_name_img = "Filtritud pilt"
    cv2.namedWindow(win_name_freq)
    cv2.namedWindow(win_name_img)

    threshold = 12
    radius = 6

    trackbars_data = {
        "Lävend": {"cur_value": threshold, "max_value": 100},
        "Raadius": {"cur_value": radius, "max_value": 100}
    }
    update_handler = TrackbarUpdateHandler(trackbars_data=trackbars_data, window_name=win_name_freq, response_latency=1)

    def trackbar_callback(x):
        threshold = trackbars_data["Lävend"]["cur_value"]
        radius = trackbars_data["Raadius"]["cur_value"]
        on_trackbar_yl6(threshold, radius, img, update_handler)

    for tb_name, tb_params in trackbars_data.items():
        cv2.createTrackbar(tb_name, win_name_freq, tb_params["cur_value"], tb_params["max_value"], trackbar_callback)

    on_trackbar_yl6(threshold, radius, img, update_handler)

    while True:
        if update_handler.update_allowed():
            threshold = trackbars_data["Lävend"]["cur_value"]
            radius = trackbars_data["Raadius"]["cur_value"]
            on_trackbar_yl6(threshold, radius, img, update_handler)
        if (cv2.waitKey(1) & 0xFF) == ord('q') or cv2.getWindowProperty(win_name_freq, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()




""" 6.2 Ülesanne """




# Funktsioon 2D Gaussi kerneli loomiseks ja selle ümberpööramiseks
def create_kernel_yl6_2(kernel_size, sigma):
    # Tagame, et kerneli suurus on alati paaritu arv
    kernel_size = 2 * kernel_size + 1
    
    # Loome 1D Gaussi kerneli
    kernel_1d = cv2.getGaussianKernel(kernel_size, sigma)
    
    # Loome 2D Gaussi kerneli, kasutades maatriksite korrutamist
    kernel_2d = np.matmul(kernel_1d, kernel_1d.T)
    
    # Leiame maksimaalse väärtuse ja pöörame kerneli ümber
    max_value = np.max(kernel_2d)
    inverted_kernel = max_value - kernel_2d
    
    # Normaliseerime pööratud kerneli vahemikku 0 kuni 1
    inverted_kernel = inverted_kernel / np.max(inverted_kernel)
    
    return inverted_kernel

def on_trackbar(val):
    kernel_size = cv2.getTrackbarPos('Kernel Size', 'Kernel Control')
    sigma = cv2.getTrackbarPos('Sigma', 'Kernel Control')
    kernel = create_kernel_yl6_2(kernel_size, sigma)
    print("Kernel Size:", kernel_size, "Sigma:", sigma)
    print(kernel)

def yl6_2():
    cv2.namedWindow('Kernel Control')

    # Algväärtused liuguritele
    kernel_size = 2  # vastab kerneli suurusele 5x5
    sigma = 1       # vastab sigma väärtusele 1.0

    # Loome liugurid
    cv2.createTrackbar('Kernel Size', 'Kernel Control', kernel_size, 10, on_trackbar)
    cv2.createTrackbar('Sigma', 'Kernel Control', sigma, 10, on_trackbar)

    # Algseisundi värskendamine
    on_trackbar(0)

    # Peatsükkel akna avatuna hoidmiseks
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def yl6_2_test():
    kernel_size = 2  # Kaardub 5x5 suuruseks
    sigma = 1.0
    expected_kernel = np.array([
        [1.0, 0.93504087, 0.88079708, 0.93504087, 1.0],
        [0.93504087, 0.64391426, 0.40081044, 0.64391426, 0.93504087],
        [0.88079708, 0.40081044, 0.0, 0.40081044, 0.88079708],
        [0.93504087, 0.64391426, 0.40081044, 0.64391426, 0.93504087],
        [1.0, 0.93504087, 0.88079708, 0.93504087, 1.0]
    ])

    kernel = create_kernel_yl6_2(kernel_size, sigma)
    if np.allclose(kernel, expected_kernel, atol=1e-8):
        print("Kerneli loomine õnnestus!")
        print("Loodud kernel:")
        print(kernel)
        print("Oodatav kernel:")
        print(expected_kernel)
    else:
        print("Kerneli loomine ebaõnnestus!")
        print("Loodud kernel:")
        print(kernel)
        print("Oodatav kernel:")
        print(expected_kernel)




    """ 6.3 Ülesanne """





# Funktsioon sageduskomponentide sujuvaks nullimiseks, kasutades konvolutsiooni
def smooth_nulling(fshift_filtered, kernel, mask):
    # Määrame töötlemisala piirid
    # y_end saab väärtuseks maatriksi ridade arvu
    y_end = fshift_filtered.shape[0]
    # x_end saab väärtuseks maatriksi veergude arvu.
    x_end = fshift_filtered.shape[1]
    
    # Arvutame nihked ridade ja veergude jaoks
    offset_y = kernel.shape[0] // 2
    offset_x = kernel.shape[1] // 2
    
    # Läbime iga piksli sageduskomponentide maatriksis
    for y in range(y_end):
        for x in range(x_end):
            # Kontrollime, kas maski väärtus on null (st. komponent tuleb nullida)
            if mask[y, x] == 0:
                # Veendume, et oleme tuuma rakendamisel maatriksi piires
                if y - offset_y >= 0 and x - offset_x >= 0 and y + offset_y < y_end and x + offset_x < x_end:
                    # Korrutame tuuma vastava piirkonna sageduskomponentide maatriksiga
                    fshift_filtered[y - offset_y:y + offset_y + 1, x - offset_x:x + offset_x + 1] *= kernel
    
    # Tagastame töödeldud sageduskomponentide maatriksi
    return fshift_filtered

# Funktsioon maski loomiseks, et määrata nullitavad sageduskomponendid
def create_filter_yl6(magnitude_spectrum, threshold, radius):
    # Kasutab cv2.threshold() funktsiooni, et nullida kõik maski elemendid, mille vastavad magnitude_spectrum väärtused ületavad määratud läve
    _, mask = cv2.threshold(magnitude_spectrum, threshold, 1, cv2.THRESH_BINARY_INV)

    rows, cols = magnitude_spectrum.shape
    center_row, center_col = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    central_area = (x - center_col)**2 + (y - center_row)**2 <= radius**2
    mask[central_area] = 1
    return mask

# Funktsioon sagedusfiltri rakendamiseks
def apply_filter_yl6(fshift, mask):
    fshift_filtered = fshift * mask
    return fshift_filtered

# Funktsioon sagedusruumi teisendamiseks koordinaatruumi
def to_image_space_yl6(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img_back

# Funktsioon sagedusruumi ja filtreeritud pildi kuvamiseks
def display_images_yl6(filtered_spectrum, filtered_image):
    filtered_magnitude_spectrum = np.log(np.abs(filtered_spectrum) + 1)
    filtered_magnitude_spectrum = cv2.normalize(filtered_magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("Filtritud sagedusruum", filtered_magnitude_spectrum)
    cv2.imshow("Filtritud pilt", filtered_image)

# Funktsioon liugurite muutmisel sagedusfiltri ja kerneli uuendamiseks ning pildi kuvamiseks
def on_trackbar_yl6_3(threshold, kernel_size, sigma, img, update_handler, radius):
    # Teostame FFT pildile
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    # Loome maski ja kerneli
    mask = create_filter_yl6(magnitude_spectrum, threshold, radius)
    kernel = create_kernel_yl6_2(kernel_size, sigma)
    
    # Rakendame kerneli sageduskomponentidele
    fshift_smoothed = smooth_nulling(fshift, kernel, mask)
    
    # Teisendame sagedusruumist tagasi koordinaatruumi
    img_filtered = to_image_space_yl6(fshift_smoothed)
    
    # Kuvame sagedusruumi ja filtreeritud pildi
    display_images_yl6(fshift_smoothed, img_filtered)

# Põhifunktsioon sagedusfiltri rakendamiseks pildile ja liugurite haldamiseks
def yl6_3():
    img_path = 'andmed/images/p09_yl_6_noisy_plant.jpg'  # Tee üles laetud pildi juurde
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Ei leitud pilti aadressil: {img_path}")
    
    win_name_freq = "Filtritud sagedusruum"
    win_name_img = "Filtritud pilt"
    cv2.namedWindow(win_name_freq)
    cv2.namedWindow(win_name_img)

    threshold = 60
    kernel_size = 5
    sigma = 1.0
    radius = 6

    # Liugurite andmed
    trackbars_data = {
        "Lävend": {"cur_value": threshold, "max_value": 255},
        "Kerneli suurus": {"cur_value": kernel_size, "max_value": 50},
        "Sigma": {"cur_value": int(sigma), "max_value": 100},
        "Raadius": {"cur_value": radius, "max_value": 100}
    }
    update_handler = TrackbarUpdateHandler(trackbars_data=trackbars_data, window_name=win_name_freq, response_latency=1)

    # Liugurite callback funktsioon
    def trackbar_callback(x):
        threshold = trackbars_data["Lävend"]["cur_value"]
        kernel_size = trackbars_data["Kerneli suurus"]["cur_value"]
        sigma = trackbars_data["Sigma"]["cur_value"]
        radius = trackbars_data["Raadius"]["cur_value"]
        on_trackbar_yl6_3(threshold, kernel_size, sigma, img, update_handler, radius)

    # Liugurite loomine
    for tb_name, tb_params in trackbars_data.items():
        cv2.createTrackbar(tb_name, win_name_freq, tb_params["cur_value"], tb_params["max_value"], trackbar_callback)

    # Esialgne kuvamine
    on_trackbar_yl6_3(threshold, kernel_size, sigma, img, update_handler, radius)

    # Peatsükkel akna avatuna hoidmiseks ja liugurite uuendamiseks
    while True:
        if update_handler.update_allowed():
            threshold = trackbars_data["Lävend"]["cur_value"]
            kernel_size = trackbars_data["Kerneli suurus"]["cur_value"]
            sigma = trackbars_data["Sigma"]["cur_value"]
            radius = trackbars_data["Raadius"]["cur_value"]
            on_trackbar_yl6_3(threshold, kernel_size, sigma, img, update_handler, radius)
        if (cv2.waitKey(1) & 0xFF) == ord('q') or cv2.getWindowProperty(win_name_freq, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

    



""" 6.4 Ülesanne """





import numpy as np
import cv2

def smooth_nulling_yl6_4(fshift_filtered, kernel, mask):
    y_end = fshift_filtered.shape[0]
    x_end = fshift_filtered.shape[1]
    
    offset_y = kernel.shape[0] // 2
    offset_x = kernel.shape[1] // 2
    
    # Loome maski, mis jälgib, millised piirkonnad on juba mõjutatud
    affected_area = np.zeros_like(mask)
    
    for y in range(y_end):
        for x in range(x_end):
            if mask[y, x] == 0:
                # Veendume, et oleme tuuma rakendamisel maatriksi piires
                if y - offset_y >= 0 and x - offset_x >= 0 and y + offset_y < y_end and x + offset_x < x_end:
                    # Kontrollime, kas piirkond on juba mõjutatud
                    if np.any(affected_area[y - offset_y:y + offset_y + 1, x - offset_x:x + offset_x + 1]):
                        continue  # Jätkame, kui piirkond on juba mõjutatud
                    
                    # Rakendame kerneli
                    fshift_filtered[y - offset_y:y + offset_y + 1, x - offset_x:x + offset_x + 1] *= kernel
                    
                    # Märgime piirkonna mõjutatuks
                    affected_area[y - offset_y:y + offset_y + 1, x - offset_x:x + offset_x + 1] = 1
    
    return fshift_filtered


def yl6_4():
    img_path = 'andmed/images/p09_yl_6_noisy_plant.jpg'  # Tee üles laetud pildi juurde
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Ei leitud pilti aadressil: {img_path}")
    
    win_name_freq = "Filtritud sagedusruum"
    win_name_img = "Filtritud pilt"
    cv2.namedWindow(win_name_freq)
    cv2.namedWindow(win_name_img)

    threshold = 60
    kernel_size = 5
    sigma = 1.0
    radius = 6

    # Liugurite andmed
    trackbars_data = {
        "Lävend": {"cur_value": threshold, "max_value": 255},
        "Kerneli suurus": {"cur_value": kernel_size, "max_value": 20},
        "Sigma": {"cur_value": int(sigma), "max_value": 100},
        "Raadius": {"cur_value": radius, "max_value": 100}
    }
    update_handler = TrackbarUpdateHandler(trackbars_data=trackbars_data, window_name=win_name_freq, response_latency=1)

    # Liugurite callback funktsioon
    def trackbar_callback(x):
        threshold = trackbars_data["Lävend"]["cur_value"]
        kernel_size = trackbars_data["Kerneli suurus"]["cur_value"]
        sigma = trackbars_data["Sigma"]["cur_value"]
        radius = trackbars_data["Raadius"]["cur_value"]
        on_trackbar_yl6_4(threshold, kernel_size, sigma, img, update_handler, radius)

    # Liugurite loomine
    for tb_name, tb_params in trackbars_data.items():
        cv2.createTrackbar(tb_name, win_name_freq, tb_params["cur_value"], tb_params["max_value"], trackbar_callback)

    # Esialgne kuvamine
    on_trackbar_yl6_4(threshold, kernel_size, sigma, img, update_handler, radius)

    # Peatsükkel akna avatuna hoidmiseks ja liugurite uuendamiseks
    while True:
        if update_handler.update_allowed():
            threshold = trackbars_data["Lävend"]["cur_value"]
            radius = trackbars_data["Raadius"]["cur_value"]
            kernel_size = trackbars_data["Kerneli suurus"]["cur_value"]
            sigma = trackbars_data["Sigma"]["cur_value"]
            radius = trackbars_data["Raadius"]["cur_value"]
            on_trackbar_yl6_4(threshold, kernel_size, sigma, img, update_handler, radius)
        if (cv2.waitKey(1) & 0xFF) == ord('q') or cv2.getWindowProperty(win_name_freq, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

def on_trackbar_yl6_4(threshold, kernel_size, sigma, img, update_handler, radius):
    # Teostame FFT pildile
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    # Loome maski ja kerneli
    mask = create_filter_yl6(magnitude_spectrum, threshold, radius)
    kernel = create_kernel_yl6_2(kernel_size, sigma)
    
    # Rakendame kerneli sageduskomponentidele
    fshift_smoothed = smooth_nulling_yl6_4(fshift, kernel, mask)
    
    # Teisendame sagedusruumist tagasi koordinaatruumi
    img_filtered = to_image_space_yl6(fshift_smoothed)
    
    # Kuvame sagedusruumi ja filtreeritud pildi
    display_images_yl6(fshift_smoothed, img_filtered)



def main():
    # yl1()
    # yl2()
    # yl2_2()
    # yl2_3()
    # yl3()
    # yl4()
    # yl5()
    # yl6()
    # yl6_2()
    # yl6_2_test()
    # yl6_3()
     yl6_4()


if __name__ == '__main__':
    main()
