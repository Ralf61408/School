import numpy as np
import tkinter as tk
from tkinter import Canvas, Button
from sklearn.preprocessing import StandardScaler
from numpy.fft import fft
import joblib

class DigitRecognizer:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=400, height=400, bg='white') # Loome lõuendi kasutajaliidese jaoks
        self.canvas.pack() # Pakime lõuendi GUI-sse
        self.points = [] # Alustame tühja punktide nimekirjaga

        # Laeme eeltreenitud mudel
        self.model = joblib.load('digit_model.pkl')

        # Seo hiire sündmused meetoditega
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.button_clear = Button(master, text="Clear", command=self.clear_all)
        self.button_clear.pack(side="bottom")
        
    def on_button_press(self, event):
        self.points = [] # Tühjendame eelnevad punktid
        self.points.append((event.x, event.y)) # Lisame esimese punkti
    
    def on_move_press(self, event): # Joonistamine
        self.canvas.create_oval(event.x - 4, event.y - 4, event.x + 4, event.y + 4, fill='black', outline='black')
        self.points.append((event.x, event.y))
    
    def on_button_release(self, event):
        # Käivitame numbri tuvastamise
        self.recognize_digit(self.points)
    
    def clear_all(self):
        # Puhastame kogu lõuendi
        self.canvas.delete("all")
    
    def recognize_digit(self, points):
        if len(points) > 1:
            # Konverteerime punktid 28x28 pildiandmeteks masinõppemudelites, MNIST andmekogu puhul
            img_data = self.points_to_image_data(points, image_size=(28, 28))
            
             # Ennustme numbri kasutades mudelit
            predicted_digit = self.model.predict([img_data])[0]
            print(f"Predicted Digit: {predicted_digit}")
            self.canvas.create_text(200, 350, text=f"Predicted Digit: {predicted_digit}", font=("Purisa", 16))

    def points_to_image_data(self, points, image_size=(28, 28)):
        """ Konverteerime punktid 28x28 normaliseeritud pildiandmeteks """
        img = np.zeros(image_size, dtype=np.float32) # Tühi pilt
        # Implementeeritud loogika punktide konverteerimiseks 28x28 pildiks
        for x, y in points:
            # Skaala punktid 28x28 ruudustikule
            x_scaled = int(x / 400 * 28)
            y_scaled = int(y / 400 * 28)
            img[y_scaled % 28, x_scaled % 28] = 1  # Määra piksel väärtuseks 1
        return img.flatten() # Tagastame pildiandmed ühe mõõtmelise massiivina
 
def main():
    root = tk.Tk()
    app = DigitRecognizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
