#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


def convert_waveform_preamble(waveform_preamble: str) -> dict:
    """
    Query and return all the waveform parameters.

    Args:
        waveform_preamble (str): string that contains the 10 waveform parameters separated by ","

    Returns:
        A dictionary that contains the following:
            int:   wav_format where 0 (BYTE), 1 (WORD) or 2 (ASC)
            int:   wav_type where 0 (NORMal), 1 (MAXimum) or 2 (RAW).
            int:   nr_of_points is an integer between 1 and 24000000 denoting the number of points you can read with a data request
            int:   nr_of_avg is the number of averages in the average sample mode and 1 in other modes.
            float: x_increment is the time difference between two neighboring points in the X direction in seconds.
            float  x_origin is the start time of the waveform data in the X direction.
            int:   x_reference is the reference time of the data point in the X direction.
            float: y_increment is the waveform increment in the Y direction.
            int:   y_origin is the vertical offset relative to the "Vertical Reference Position" in the Y direction.
            int:   y_reference is the vertical reference position in the Y direction.
    """
    waveform_preamble = waveform_preamble.split(",")
    assert len(waveform_preamble) == 10

    wav_format, wav_type, wav_points, wav_count, x_reference, y_origin, y_reference = (
        int(val) for val in waveform_preamble[:4] + waveform_preamble[6:7] + waveform_preamble[8:10]
    )
    x_increment, x_origin, y_increment = (
        float(val) for val in waveform_preamble[4:6] + waveform_preamble[7:8]
    )
    return {
        "format": wav_format,
        "type": wav_type,
        "nr_of_points": wav_points,
        "nr_of_avg": wav_count,
        "x_increment": x_increment,
        "x_origin": x_origin,
        "x_reference": x_reference,
        "y_increment": y_increment,
        "y_origin": y_origin,
        "y_reference": y_reference,
    }


def create_x_axis_values(preamble_dict):
    x1 = preamble_dict["x_increment"]
    x2 = preamble_dict["x_origin"]
    wav_points = preamble_dict["nr_of_points"]

    xjaotus = np.arange(0, wav_points * x1, x1) +x2
    #0 alguspunkt, wav_points * 1 lõpppunkt, x1 kui palju lisab ja lõpuks et õige scale oleks siis +x2

    print(xjaotus)

    return xjaotus


def convert_data_to_volts(data, preamble_dict):
    y1 = preamble_dict["y_increment"]
    y2 = preamble_dict["y_origin"]
    y3 = preamble_dict["y_reference"]

    yjaotus = (data - y2 - y3) * y1
    ##data.setData(y = yjaotus, x = xjaotus)

    return yjaotus
