#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


class OverlapAdd:
    def __init__(self, win_size, hop_size, output_size, convert_to_frequency_domain, process, convert_to_time_domain, extra_params={}) -> None:
        self.win_size = win_size
        self.hop_size = hop_size
        self.output_size = output_size
        self.convert_to_frequency_domain = convert_to_frequency_domain
        self.process = process
        self.convert_to_time_domain = convert_to_time_domain
        self.extra_params = extra_params


    def run(self, data):
        # Initsialiseerige tulemussignaal nullidega nii, et selle pikkus oleks output_size
        output = np.zeros(self.output_size)
        # Käige läbi kõik sisendsignaali lõigud kasutades muutujaid win_size ja hop_size
        for start in range(0, len(data), self.hop_size):
            end = start + self.win_size
            #Võetakse sisendsignaalist lõik alates start kuni end. Kui end indeks ületab sisendsignaali pikkuse, siis lõigu lõppu lisatakse nullid nii, et lõigu pikkus oleks täpselt win_size.
            #data_chunk = data[start:end] if end <= len(data) else np.pad(data[start:], (0, self.win_size - len(data) + start), 'constant')
            data_chunk = data[start:end]
            # Viige lõik sagedusruumi kasutades convert_to_frequency_domain() funktsiooni.
            frequency_domain_chunk = self.convert_to_frequency_domain(data_chunk, self.extra_params)
            # Sooritage sagedusruumi viidud lõigul operatsioon kasutades process() funktsiooni.
            processed_chunk = self.process(frequency_domain_chunk, self.extra_params)
            # Tooge tulemuse lõik tagasi aegruumi kasutades convert_to_time_domain() funktsiooni.
            time_domain_chunk = self.convert_to_time_domain(processed_chunk, self.extra_params)
            
            actual_len = min(len(time_domain_chunk), self.output_size - start)
            
            # Liidan uue töödeldud osa tulemussignaaliga, arvestades võimalikku ülekattuvust
            if start + actual_len <= self.output_size:
                output[start:start+actual_len] += time_domain_chunk[:actual_len]
            else:  # Kui ületame väljundi suuruse
                output[start:] += time_domain_chunk[:self.output_size - start]

        return output[:self.output_size]


