import numpy as np
import cv2
import joblib
from sklearn.datasets import fetch_openml

# Eeltöötluse funktsioon
def eeltootle_pilt(pilt):
    pilt = pilt.astype(np.uint8)
    
    #Teisendame halltoonipildi binaarpildiks. 
    # Kõik pikseliväärtused, mis on suuremad või võrdsed 127-ga, määratakse väärtusele 255 (valge),
    # ja kõik väiksemad väärtused saavad 0 (must).
    _, binariseeritud = cv2.threshold(pilt, 127, 255, cv2.THRESH_BINARY)  
    
    kernel = np.ones((3, 3), np.uint8)  # Loome 3x3 suurusega kerneli, mis on vajalik järgnevateks morfoloogilisteks operatsioonideks.
    
    # Rakendame laiendamist, mis suurendab valgete piirkondade suurust pildil. 
    # See aitab ühendada lähedal asuvaid valgeid alasid, et moodustada suuremaid objekte, 
    # mis on kasulik väikeste tühimike või aukude täitmisel.
    paksendatud = cv2.dilate(binariseeritud, kernel, iterations=1)  
   
    # Rakendab avamisoperatsiooni, mis on erosioon laiendatud (dilate'itud) objektile.
    # See eemaldab valgest piirkonnast väljaulatuvad osad ja vähendab müra, parandades objekti piire.
    avatud = cv2.morphologyEx(paksendatud, cv2.MORPH_OPEN, kernel)  
    
    # Rakendab sulgemisoperatsiooni, see aitab täita väikesed augud ja lõhed objektides 
    suletud = cv2.morphologyEx(avatud, cv2.MORPH_CLOSE, kernel)  
    
    return suletud 

# Kontuuri punktide normaliseerimise funktsioon
def normaliseeri_punktid(kontuur):
    # Muudame kontuuri andmestruktuuri ühedimensioonilisest massiivist  kahedimensiooniliseks,
    # kus esimene veerg sisaldab x-koordinaate ja teine veerg y-koordinaate. 
    kontuur = kontuur.reshape(-1, 2)  
    
    x = kontuur[:, 0]  # Eraldame kõik x-koordinaadid
    y = kontuur[:, 1]  # Eraldame kõik y-koordinaadid

    wd = np.max(x) - np.min(x)  # Arvutame kõige kaugemate x-koordinaatide vahe, saades objekti laiuse.
    hg = np.max(y) - np.min(y)  # Arvutame kõige kaugemate y-koordinaatide vahe, saades objekti kõrguse.

    # Normaliseerib punktid mõõtkavasse 0 kuni 100, punktidele ühtlase skaala andmine, valem 1 ja valem 2
    x_n = 100 * (x - np.min(x)) / wd  # Skaleerib x-koordinaadid, kus 0 on miinimum x väärtus ja 100 on maksimum.
    y_n = 100 * (y - np.min(y)) / hg  # Skaleerib y-koordinaadid, kus 0 on miinimum y väärtus ja 100 on maksimum.

    return x_n, y_n  

# Fourier kirjeldajate arvutamine vastavalt valemile 3
def arvuta_fourier_kirjeldajad(x_n, y_n):
    N = len(x_n)  #Normaliseeritud andmete pikkus
    k = np.arange(N)  # Loome järjendi väärtustega 0 kuni N-1, mis esindab Fourier kirjeldajate indeksid
    u = k.reshape((N, 1))  # Muudame järjendi veeruvektoriks (Nx1)
    
    # Arvutame reaalsed ja imaginaarsed osad Fourier' transformatsiooniks
    # R_F arvutab reaalse osa Fourier' koefitsientidest. 
    # Siin kasutame kosinust x_n ja siinus y_n komponentide jaoks.
    R_F = (1/N) * np.sum(x_n * np.cos(2 * np.pi * k * u / N) + y_n * np.sin(2 * np.pi * k * u / N), axis=1)
    
    # I_F arvutab imaginaarse osa Fourier' koefitsientidest.
    # Siin kasutame siinus x_n ja kosinust y_n komponentide jaoks.
    I_F = (1/N) * np.sum(x_n * np.sin(2 * np.pi * k * u / N) - y_n * np.cos(2 * np.pi * k * u / N), axis=1)
   
    
    # Arvutame Fourier' kirjeldajad, mis on reaalse ja imaginaarse osa ruutude summa ruutjuur
    F_n = np.sqrt(R_F**2 + I_F**2)
    
    return F_n[:30]  # Tagastame ainult esimesed 30 koefitsienti, kuna need sisaldavad piisavalt infot kuju kohta


# Kontuuri omaduste leidmise funktsioon
def leia_kontuuri_omadused(pilt):
    eeltoodeldud_pilt = eeltootle_pilt(pilt)  # Eeltöötleme pildi, et saada parem kontuuride leidmise tulemus
    kontuurid, _ = cv2.findContours(eeltoodeldud_pilt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #Leiame kontuurid

    if not kontuurid:  # Kontrollime, kas kontuuride loend on tühi
        return np.zeros(30)  # Kui pole kontuure, tagastame nullvektori

    max_kontuur = max(kontuurid, key=cv2.contourArea)  # Leia suurim kontuur pindala järgi

    # Teeb kontuuri punktidest ligikaudse polügooni, lihtsustab kontuuri
    proovitav_kontuur = cv2.approxPolyDP(max_kontuur, 3, True)
    if len(proovitav_kontuur) < 30:
        # Kui punkte pole piisavalt, duplitseerime esimesed punktid kuni saame 30 punkti
        proovitav_kontuur = np.vstack([proovitav_kontuur, np.repeat(proovitav_kontuur[:1], 30 - len(proovitav_kontuur), axis=0)])
    proovitav_kontuur = proovitav_kontuur[:30]  # Võtame esimesed 30 punkti

    #Normaliseerime punktid, et need oleksid võrdluseks sobival kujul
    x_n, y_n = normaliseeri_punktid(proovitav_kontuur)

    # Arvutame Fourier' kirjeldajad, et saada kontuuri omadused
    omadused = arvuta_fourier_kirjeldajad(x_n, y_n)
    
    return omadused

def loo_baas_omadused_ja_klassid(X, y):
    baas_omadused = []  # List baasomaduste hoidmiseks
    baas_klassid = []  # List baasklasside hoidmiseks

    for number in range(10):  # Iga numbri (0-9) jaoks
        numbri_omadused = X[y == str(number)]  # Filtreerime välja kõik näidised, mis vastavad hetkelisele numbrile
        baas_omadused.extend(numbri_omadused[:500])  # Võtame iga numbri kohta 500 näidet ja lisame need baasomaduste listi
        baas_klassid.extend([number] * 500)  # Lisame 500 korda numbri klassi baasklasside listi

    return baas_omadused, baas_klassid  # Tagastame baasomaduste ja baasklasside listid

# Mudeli treenimise ja salvestamise funktsioon
def treeni_ja_salvesta_mudel():
    # Laadime MNIST andmestiku
    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False) 
    # Muudame andmed 28x28 kujutisteks, kuna andmed on algselt ühe pika vektorina
    X = X.reshape((-1, 28, 28))
    # Töötleme iga kujutist, et leida kontuuri omadused
    X_omadused = np.array([leia_kontuuri_omadused(x) for x in X]) 
    # Loome viiteomadused ja klassid, kasutades eelnevalt määratletud funktsiooni
    baas_omadused, baas_klassid = loo_baas_omadused_ja_klassid(X_omadused, y) 
    # Salvestame viiteomadused ja klassid faili, et neid hiljem kasutada
    joblib.dump((baas_omadused, baas_klassid), 'numbrid.pkl') 
    print("Mudel on treenitud ja salvestatud.")

# Peamine funktsioon
def main():
    # Treenime ja salvestame mudeli
    treeni_ja_salvesta_mudel()

if __name__ == "__main__":
    main() 