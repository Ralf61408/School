import cv2  # Importib OpenCV teegi, mis on vajalik piltide töötlemiseks
import os  # Importib os teegi, mis võimaldab failisüsteemi operatsioone
import numpy as np  # Importib NumPy teegi, mis on vajalik numbriliste arvutuste jaoks
from timeit import default_timer as timer  # Importib timeri, mis võimaldab mõõta aega

# Määratleb kausta, kuhu pilt salvestatakse, kasutades praeguse faili asukohta
base_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(base_path, "andmed/images")

def yl1():

    # Määratleb pildi mõõtmed (nt. 100x100)
    height = 800
    width = 800

    # Loob pildi, kus iga piksel on BGR väärtusega [145, 237, 237]
    uniform_color_image = np.full((height, width, 3), [145, 237, 237], dtype=np.uint8)

    # Määratleb täieliku tee pildifaili jaoks
    image_path = os.path.join(images_path, "uniform_color_image.jpg")

    # Salvestab pildi
    cv2.imwrite(image_path, uniform_color_image)
    print(f"Pilt salvestati aadressile: {image_path}")

    # Loeb pildi ja kuvab selle
    goal_img = cv2.imread(image_path)
    if goal_img is None:
        print("Pildi laadimine ebaõnnestus aadressilt:", image_path)

    # Kuvab NumPy abil saadud halltoonide pildi aknas nimega "grayscalenumpypilt"
    cv2.imshow("alguses", goal_img)

    print("katsetus0", goal_img)
    
    # Saab pildi mõõtmed (kõrgus, laius ja kanalite arv)
    height, width, _ = goal_img.shape

    # Loob tühja halltoonide pildi, mille suurus vastab algsele pildile
    gray_image = np.zeros((height, width), dtype=np.uint8)
    
    # Alustab ajamõõtmist enda kirjutatud tsükli jaoks
    time_own = timer()
    
    # Kahe tsükliga minnakse üle kõikide piksli koordinaatide (i, j)
    for i in range(height):
        for j in range(width):
            # Saab värvikomponendid (punane, roheline, sinine) igast pikslikohast
            red = goal_img[i, j, 2]
            green = goal_img[i, j, 1]
            blue = goal_img[i, j, 0]
            # Arvutab halltooni väärtuse, kasutades punase, rohelise ja sinise värvikomponendi kaalu
            gray = 0.299 * red + 0.587 * green + 0.114 * blue
            # Määrab halltooni väärtuse halltoonide pildile
            gray_image[i, j] = int(gray)
    
    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_own_elapsed = timer() - time_own

    print("for aeg", time_own_elapsed)
    
    # Kuvab saadud halltoonide pildi aknas nimega "grayscalepilt"
    cv2.imshow("grayscalepilt", gray_image)
    
    # Alustab ajamõõtmist NumPy teegi jaoks
    time_numpy = timer()
    
    # Kasutab NumPy vektoriseerimist halltoonide pildi arvutamiseks ühe operatsiooniga
    gray_numpy_image = 0.299 * goal_img[:, :, 2] + 0.587 * goal_img[:, :, 1] + 0.114 * goal_img[:, :, 0]
    
    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_numpy_elapsed = timer() - time_numpy

    print("numpy aeg", time_numpy_elapsed)
    
    # Teisendab NumPy halltoonide pildi uint8 tüüpi
    gray_numpy_image = gray_numpy_image.astype(np.uint8)
    
    # Kuvab NumPy abil saadud halltoonide pildi aknas nimega "grayscalenumpypilt"
    cv2.imshow("grayscalenumpypilt", gray_numpy_image)
    
    # Hoidke aknad avatuna, kuni kasutaja vajutab 'q' klahvi
    while cv2.getWindowProperty('grayscalenumpypilt', cv2.WND_PROP_VISIBLE) >= 1:
        if (cv2.waitKey(10) & 0xFF) == ord("q"):
            break
    # Sulgeb kõik aknad
    cv2.destroyAllWindows()


def main():
    yl1()


if __name__ == '__main__':
    main()
