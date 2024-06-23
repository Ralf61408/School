import numpy as np
import tkinter as tk
from tkinter import Canvas, Button
import joblib
from Treeningmudel import leia_kontuuri_omadused

class NumbriTuvastaja:
    def __init__(self, master):
        # Algatab peamise akna ja lõuendi, kus kasutaja saab joonistada
        self.master = master
        self.canvas = Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()
        self.points = []
        # Tühjenda nupp
        self.button_clear = Button(master, text="Tühjenda", command=self.koik_tuhjaks)
        self.button_clear.pack(side="bottom")
        
        # Seome hiire vajutamise, liigutamise ja vabastamise sündmused
        self.canvas.bind("<ButtonPress-1>", self.nupu_vajutus)  # Hiire nupu vajutus
        self.canvas.bind("<B1-Motion>", self.liikumise_vajutus)  # Hiire liikumine nupu vajutamise ajal
        self.canvas.bind("<ButtonRelease-1>", self.nupu_vabastus)  # Hiire nupu vabastamine
        
        # Laadige mudel, mis sisaldab baasomadusi ja -klasse
        self.model = joblib.load('numbrid.pkl')

        """
        Siin kogutakse kasutaja poolt joonistatud kujundi punktid. 
        See on esimene samm, mis võimaldab reaalajas digitaalset tuvastamist, 
        kus kasutaja joonistab numbri graafikalauaga.
        """

    # Funktsioon, mis käivitatakse hiire vajutamisel
    def nupu_vajutus(self, event):
        self.points = []  # Tühjendame eelnevad punktid
        self.points.append((event.x, event.y))  # Lisame esimese punkti
    
    # Funktsioon, mis käivitatakse hiire liikumisel
    def liikumise_vajutus(self, event):
        # Joonistab ovaali igas hiire liikumise punktis
        self.canvas.create_oval(event.x - 4, event.y - 4, event.x + 4, event.y + 4, fill='black', outline='black')
        self.points.append((event.x, event.y))  # Lisame uue punkti
    
    # Funktsioon, mis käivitatakse hiire vabastamisel
    def nupu_vabastus(self, event):
        self.tuvasta_number(self.points)  # Käivitame numbri tuvastamise
    
    # Funktsioon, mis tühjendab canvase
    def koik_tuhjaks(self):
        self.canvas.delete("all")  # Kustutab canvaselt kontuurid

    
    # Funktsioon, mis tuvastab joonistatud numbri
    def tuvasta_number(self, punktid):
        if len(punktid) > 1:  # Kontrollime, et punktide arv on suurem kui 1
            # Muudame punktid 28x28 pildiks ja töötleme neid
            img_andmed = self.punktid_pildiks(punktid, pildi_suurus=(28, 28))  # Muudame kasutaja poolt joonistatud punktid 28x28 piksliseks pildiks
            img_andmed = img_andmed.reshape(28, 28).astype(np.uint8)  # Veendume, et pilt on õiges formaadis
            img_omadused = leia_kontuuri_omadused(img_andmed)  # Kasutame eeltöötluse funktsiooni, et leida kontuuri omadused pildist
            
            # Saadud omadusi kasutades teeme ennustuse
            ennustatud_number = self.ennusta_klass(img_omadused)  # Ennustame numbri, kasutades leitud omadusi
            print(f"Ennustatud number: {ennustatud_number}")  # Prindime ennustatud numbri konsooli
            # Kuvame lõuendil ennustatud numbri
            self.canvas.create_text(200, 350, text=f"Ennustatud number: {ennustatud_number}", font=("Purisa", 16))  # Kuvame lõuendil teksti, mis näitab ennustatud numbrit

    def ennusta_klass(self, omadused):
        # Ennustame numbri, võrreldes omadusi baasomadustega
        baas_omadused_list, baas_klassid_list = self.model  # Laadime mudelis salvestatud baasomadused ja klassid
        min_kaugus = float('inf')  #Minimaalse kauguse määramine lõpmatusena, et leida lähim omadus
        ennustatud_klass = None  #Ennustatud klassi sisestamine tühja väärtusega

        # Läbime kõik baasomadused ja nendele vastavad klassid
        for baas_omadus, baas_klass in zip(baas_omadused_list, baas_klassid_list):
            #võrdleme vektoreid (Eukleidiline kauguse abil)
            kaugus = np.linalg.norm(np.array(baas_omadus) - omadused)
            
            # Kui arvutatud kaugus on väiksem kui senine minimaalne kaugus, uuendame minimaalse kauguse ja ennustatud klassi
            if kaugus < min_kaugus:
                min_kaugus = kaugus  # Uuendame minimaalse kauguse
                ennustatud_klass = baas_klass  # Uuendame ennustatud klassi

        return ennustatud_klass  


    # Funktsioon, mis teisendab punktid pildiks
    def punktid_pildiks(self, points, pildi_suurus=(28, 28)):
        # Loome nullidega täidetud pildi, mille suurus on 28x28
        img = np.zeros(pildi_suurus, dtype=np.uint8)
        # Läbime kõik punktid, mille kasutaja joonistas
        for x, y in points:
            # Skaleerime x ja y koordinaadid 400x400 lõuendilt 28x28 pildile
            x_skaleerimine = int(x / 400 * 28)
            y_skaleerimine = int(y / 400 * 28)
            # Määrame skaleeritud koordinaatidele väärtuse 255 (valge)
            # % 28 tagab, et koordinaadid jäävad pildi mõõtmetesse (0-27)
            img[y_skaleerimine % 28, x_skaleerimine % 28] = 255
            
        return img

def main():
    #Loome Tkinteri peamise akna
    root = tk.Tk()
    
    #Canvase aktiveerimine peamise aknaga
    app = NumbriTuvastaja(root)
    
    #Hoiame akent avatuna
    root.mainloop()

if __name__ == "__main__":
    main()