#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from dst.fourier.fft import fft, ifft


def convert_to_frequency_domain(data, extra_params):

    N = len(data)
    padded_length = extra_params['padded_length']
    pad_width = (0, int(padded_length - N))
    padded_data = np.pad(data, pad_width, 'constant')
    return fft(padded_data)

def process(data, extra_params):
    return data * extra_params['impulse_response_freq']

def convert_to_time_domain(data, extra_params):
    # Teisendage konvolutsiooni tulemus tagasi aegruumi
    return np.real(ifft(data))

