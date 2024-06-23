#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time


class TrackbarUpdateHandler:
    def __init__(self, trackbars_data, window_name, response_latency) -> None:
        self.window_name = window_name
        self.trackbars_data = trackbars_data
        self.tb_prev_values = [tb_params["cur_value"] for tb_params in trackbars_data.values()] # Mugavusmuutuja võrdluste hõlbustamiseks

        self.response_latency = response_latency # Sekundites
        self.last_request_time = time.time()
        self.is_interval_started = True
        self.is_update_allowed = True


    def start_interval(self, request_time: float) -> None:
        """
        Registreerib latentsusperioodi algusaja ja alustamise fakti.

        Argumendid:
        request_time -- latentsusperioodi algusaeg

        Tagastab:
            None
        """
        self.last_request_time = request_time
        self.is_interval_started = True


    def update_allowed(self) -> bool:
        """
        Kontrollib, kas toimingute tegemine on lubatud.
        Selleks kontrollib, kas vähemalt ühe liuguri positsioon on muutunud
        ning kas muutusest on möödunud määratud latentsusperioodi jagu aega.

        Argumendid:
            ei ole

        Tagastab:
            self.is_update_allowed -- tõeväärtus, kas toimingud on lubatud
        """
        tb_cur_values = []
        # Küsime liugurite hetkeväärtused
        for key in self.trackbars_data.keys():
            self.trackbars_data[key]["cur_value"] = cv2.getTrackbarPos(key, self.window_name)
            tb_cur_values.append(self.trackbars_data[key]["cur_value"])

        # Kui mõne liuguri väärtus on muutunud, siis alustame latentsusperioodi
        if tb_cur_values != self.tb_prev_values:
            self.start_interval(time.time())
            self.tb_prev_values = tb_cur_values[:] # Uuendame eelmiste liuguriväärtuste järjendit

        # Kas on möödunud piisavalt aega viimasest liuguriliigutusest?
        if self.is_interval_started and time.time() - self.last_request_time > self.response_latency:
            self.is_update_allowed = True
            self.is_interval_started = False
        else:
            self.is_update_allowed = False

        return self.is_update_allowed


def main():
    img = np.zeros((100, 100), dtype=np.uint8) # Loome tühja pildi
    win_name = "Pilt"
    cv2.namedWindow(win_name) # Loome akna, kus pilti ja liugureid kuvada
    # Lisame aknasse liugurid, mis muudavad soovitud väärtusi
    # Hoiame liugurite andmeid sõnastikus kujul {"nimi": parameetrid}
    trackbars_data = {"heledus": {"cur_value": 0, "max_value": 255},
                      "katkine rida": {"cur_value": 5, "max_value": 99}}

    for tb_name, tb_params in trackbars_data.items():
        cv2.createTrackbar(tb_name, win_name, tb_params["cur_value"], tb_params["max_value"], lambda x: None)

    update_handler = TrackbarUpdateHandler(trackbars_data=trackbars_data, window_name=win_name, response_latency=1)

    # Selleks, et jooksvaid muutusi kuvada, on mõistlik kasutada tsüklit.
    # Tasub mõelda, milline osa programmist peab olema tsükli sees
    # ja mida on tarvis teha vaid ühe korra (mis ei sõltu lävendist).
    while True:
        # Piirame pildi uuendamise sagedust
        if update_handler.update_allowed():
            # Määrame pildi iga piksli väärtuseks liuguri väärtuse
            img[:] = trackbars_data["heledus"]["cur_value"]
            img[trackbars_data["katkine rida"]["cur_value"]] = 0
            # Kuvame pilti aknas "Pilt"
            cv2.imshow("Pilt", img)

        # Q-tähe vajutamise või akna sulgemise korral programm sulgub
        if (cv2.waitKey(1) & 0xFF) == ord('q') or cv2.getWindowProperty("Pilt", cv2.WND_PROP_VISIBLE) < 1:
            break

    # Programmi lõpus suletakse kõik aknad
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
