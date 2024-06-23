#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Phasor:
    def __init__(self, frequency, magnitude, phase, real=None, imaginary=None):
        self.frequency = frequency   # Faasori sagedus
        self.magnitude = magnitude   # Faasori magnituud
        self.phase = phase           # Faasori faasinihe
        self.real = real             # Faasori kompleksarvulise esituse reaalosa
        self.imaginary = imaginary   # Faasori kompleksarvulise esituse imaginaarosa


    # __repr__ funktsioon Python'is annab võimaluse valida, millist informatsiooni me soovime
    # näha, kui me prindime objekti käsureale või kasutame silurit.
    def __repr__(self) -> str:
        return f"Phasor{{ freq: {self.frequency}, mag: {self.magnitude}, phase: {self.phase}, complex: {self.real} + {self.imaginary}j }}"
