#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from dst.fourier.fft import fft
from dst.fourier.overlapadd.OverlapAdd import OverlapAdd
from dst.fourier.overlapadd.convolution_dependencies import convert_to_frequency_domain, process, convert_to_time_domain


def overlap_add_section_lengths(long_length, short_length):
    """
    See funktsioon võtab sisendiks kahe ositi konvoleeritava signaali pikkused ning tagastab
    arvutatud ositi konvoleerimise jaoks vajalikud parameetrid.

    Sisendid:
    long_length: Pikema signaali pikkus
    short_length: Lühema signaali pikkus

    Tagastab:
    result_length: Konvolutsiooni tulemuse pikkus
    intermediate_length: Ositi konvoleerimise ühe etapi tulemuse pikkus
    long_slice_length: Pikema signaali ühe tüki pikkus
    """
    result_length = long_length + short_length - 1
    intermediate_length = 2**(np.ceil(np.log2(short_length)) + 1)
    long_slice_length = intermediate_length - short_length + 1
    #print("aaaa", result_length, intermediate_length, long_slice_length)
    return result_length, intermediate_length, long_slice_length


def convolve_1d_fd(long_signal, short_signal):
    """
    See funktsioon võtab sisendiks kaks ajadomeenis olevat reaalarvulist signaali
    ja teostab nende sagedusruumis ositi konvoleerimise kasutades OverlapAdd
    klassi.

    Sisendid:
    long_signal: reaalarvuline signaal ajadomeenis
    short_signal: reaalarvuline signaal ajadomeenis

    Tagastab:
    output: konvoleeritud reaalarvuline signaal ajadomeenis
    """

    # Esmalt arvutame vajalikud pikkused
    result_length, intermediate_length, long_slice_length = overlap_add_section_lengths(len(long_signal), len(short_signal))

        # Konverteerin lühike signaal sagedusruumi, kasutades extra_params parameetreid
    extra_params_for_conversion = {'padded_length': intermediate_length}
    short_signal_freq = convert_to_frequency_domain(short_signal, extra_params_for_conversion)
    
    # Defineerin extra_params parameetrid OverlapAdd klassi jaoks
    extra_params = {
        'padded_length': intermediate_length,
        'impulse_response_freq': short_signal_freq
    }
    
    # Veenduge, et win_size, hop_size ja output_size on täisarvud
    oa = OverlapAdd(
        win_size=int(long_slice_length),
        hop_size=int(long_slice_length),
        output_size=int(result_length),
        convert_to_frequency_domain=convert_to_frequency_domain,
        process=process,
        convert_to_time_domain=convert_to_time_domain,
        extra_params=extra_params
    )
    
    return oa.run(long_signal)
