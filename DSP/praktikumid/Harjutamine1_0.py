import cv2
import os
import numpy as np
from timeit import default_timer as timer
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

# Määratleb kausta, kuhu pilt salvestatakse, kasutades praeguse faili asukohta
base_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(base_path, "andmed/images")

# Funktsioon, mis rakendab valemit
def apply_formula(pixel_value, alpha):
    return ((pixel_value / 255) ** alpha) * 255

def yl1():
    # Määratleb pildi mõõtmed (nt. 800x800)
    height = 800
    width = 800
    alpha = 0.5  # Määratleb eksponendi väärtuse

    # Loob pildi, kus iga piksel on BGR väärtusega [145, 237, 237]
    uniform_color_image = np.full((height, width, 3), [145, 237, 237], dtype=np.uint8)

    # Määratleb täieliku tee pildifaili jaoks
    image_path = os.path.join(images_path, "uniform_color_image.jpg")

    # Salvestab pildi ja loeb selle kohe tagasi
    cv2.imwrite(image_path, uniform_color_image)
    goal_img = cv2.imread(image_path)
    
    if goal_img is None:
        print("Pildi laadimine ebaõnnestus aadressilt:", image_path)
        return

    cv2.imshow("alguses", goal_img)
    
    # Saab pildi mõõtmed (kõrgus, laius ja kanalite arv)
    height, width, kanalid = goal_img.shape
    
    ### For-tsüklite meetod ###
    # Alustab ajamõõtmist for-tsüklite jaoks
    time_for = timer()
    
    # Kasutab for-tsükleid, et rakendada valemit punase komponendi väärtusele
    new_image_for = goal_img.copy()
    for i in range(height):
        for j in range(width):
            new_image_for[i, j, 2] = apply_formula(new_image_for[i, j, 2], alpha)

    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_for_elapsed = timer() - time_for
    print("For-tsükli aeg", time_for_elapsed)

    # Kuvab saadud uue pildi aknas nimega "uus pilt For-tsükkel"
    cv2.imshow("uus pilt For-tsükkel", new_image_for)

    ### NumPy vektoriseerimise meetod ###
    # Alustab ajamõõtmist NumPy vektoriseerimise jaoks
    time_numpy = timer()
    
    # Kasutab NumPy vektoriseerimist, et rakendada valemit punase komponendi väärtusele
    new_image_numpy = goal_img.copy()
    new_image_numpy[:, :, 2] = apply_formula(new_image_numpy[:, :, 2], alpha)

    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_numpy_elapsed = timer() - time_numpy
    print("NumPy aeg", time_numpy_elapsed)

    # Kuvab saadud uue pildi aknas nimega "uus pilt NumPy"
    cv2.imshow("uus pilt NumPy", new_image_numpy)
    
    # Hoidke aknad avatuna, kuni kasutaja vajutab 'q' klahvi
    while cv2.getWindowProperty('uus pilt NumPy', cv2.WND_PROP_VISIBLE) >= 1 or cv2.getWindowProperty('uus pilt For-tsükkel', cv2.WND_PROP_VISIBLE) >= 1:
        if (cv2.waitKey(10) & 0xFF) == ord("q"):
            break
    # Sulgeb kõik aknad
    cv2.destroyAllWindows()



### Lisame koodi juhuslike piltide genereerimise, töötlemise ja graafikule kuvamise jaoks

def process_image(image, alpha):
    height, width, kanalid = image.shape
    print("a", height, width)
    
    ### For-tsüklite meetod ###
    # Alustab ajamõõtmist for-tsüklite jaoks
    time_for = timer()
    
    # Kasutab for-tsükleid, et rakendada valemit punase komponendi väärtusele
    for i in range(height):
        for j in range(width):
            image[i, j, 2] = apply_formula(image[i, j, 2], alpha)

    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_for_elapsed = timer() - time_for

    ### NumPy vektoriseerimise meetod ###
    # Alustab ajamõõtmist NumPy vektoriseerimise jaoks
    time_numpy = timer()
    
    # Kasutab NumPy vektoriseerimist, et rakendada valemit punase komponendi väärtusele
    new_image_numpy = image.copy()
    new_image_numpy[:, :, 2] = apply_formula(new_image_numpy[:, :, 2], alpha)

    # Lõpetab ajamõõtmise ja arvutab möödunud aja
    time_numpy_elapsed = timer() - time_numpy

    return time_for_elapsed, time_numpy_elapsed

def generate_random_images_with_sizes(num_images, min_size, max_size):
    # Genereerib lineaarse vahemiku suurused min_size ja max_size vahel ning teisendab need täisarvudeks
    sizes = np.linspace(min_size, max_size, num_images).astype(int)
    
    # Loob tühja nimekirja, kuhu salvestatakse juhuslikud pildid
    random_images = []
    
    # Itereerib läbi suuruste ja genereerib juhusliku pildi iga suuruse jaoks
    for size in sizes:
        # Genereerib juhusliku pildi, kus iga pikseli väärtus on vahemikus 0 kuni 255
        random_image = np.random.randint(0, 256, (size, size, 3), dtype=np.uint8)
        # Lisab genereeritud pildi nimekirja
        random_images.append(random_image)
    
    # Tagastab nimekirja juhuslike piltidega
    return random_images

def plot_times(for_times, numpy_times):
    # Loob Qt rakenduse
    app = QtWidgets.QApplication([])
    # Loob graafiku akna
    win = pg.GraphicsLayoutWidget(show=True, title="Processing Times")
    # Lisab graafiku aknasse
    plot = win.addPlot(title="Processing Times")
    # Seadistab y-telje sildi
    plot.setLabel('left', 'Time (s)')
    # Seadistab x-telje sildi
    plot.setLabel('bottom', 'Image Index')

    # Joonistab for-tsüklitega töötlemise ajad punaste punktidega graafikule
    plot.plot(range(len(for_times)), for_times, pen='r', symbol='o', symbolBrush='r', name="For Loop Times")
    # Joonistab NumPy vektoriseerimisega töötlemise ajad siniste punktidega graafikule
    plot.plot(range(len(numpy_times)), numpy_times, pen='b', symbol='o', symbolBrush='b', name="NumPy Times")

    # Käivitab Qt rakenduse, et kuvada graafik
    QtWidgets.QApplication.instance().exec_()

def generate_and_process_random_images():
    # Määratleb, mitu juhuslikku pilti genereeritakse
    num_images = 10
    # Määratleb pildi suuruste vahemiku (minimaalne ja maksimaalne suurus)
    min_size, max_size = 100, 1000
    # Genereerib juhuslikud pildid määratud suurustega
    random_images = generate_random_images_with_sizes(num_images, min_size, max_size)
    

    # Loob tühjad nimekirjad for-tsüklitega ja NumPy vektoriseerimisega töötlemise aegade jaoks
    for_times = []
    numpy_times = []

    # Itereerib läbi genereeritud piltide
    for img in random_images:
        # Töötleb pildi ja mõõdab ajad for-tsüklite ja NumPy vektoriseerimise jaoks
        for_time, numpy_time = process_image(img, alpha=0.5)
        # Lisab töötlemise ajad vastavatesse nimekirjadesse
        for_times.append(for_time)
        numpy_times.append(numpy_time)

    # Kuvab töötlemise ajad graafikul
    plot_times(for_times, numpy_times)


def main():
    yl1()
    generate_and_process_random_images()

if __name__ == '__main__':
    main()

