#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from numpy import sqrt


def algebraic_to_exponent(c):
    """
    Funktsioon, mis teisendab kompleksarve algebraliselt kujult eksponentkujule.

    Argumendid:
    c -- kompleksarv algebralisel kujul või np.array mitme kompleksarvuga

    Tagastab:
        tuple(magnituud või magnituudide massiiv, faas või faaside massiiv)
    """

    magnituud = sqrt(c.real**2 + c.imag**2)
    faas = np.arctan2(c.imag, c.real)
    #faas = (np.angle(c))
    return magnituud, faas
    


def exponent_mult(r1, theta1, r2, theta2):
    """
    Funktsioon, mis korrutab omavahel kaks eksponentkujul olevat kompleksarvu.

    Argumendid:
    r1 -- esimese kompleksarvu magnituud
    theta1 -- esimese kompleksarvu faas
    r2 -- teise kompleksarvu magnituud
    theta2 -- teise kompleksarvu faas

    Tagastab:
        tuple(magnituud, faas) -- kompleksarv eksponentkujul
    """
    tuple = r1*r2, theta1+theta2
    return tuple


def exponent_to_algebraic(r, theta):
    """
    Funktsioon, mis teisendab kompleksarve eksponentkujult algebralisele kujule.

    Argumendid:
    r -- kompleksarvu magnituud või np.array mitme magnituudiga
    theta -- kompleksarvu faas või np.array mitme faasiga

    Tagastab:
        kompleksarv algebralisel kujul või np.array kompleksarvudest
    """
    return complex(r*np.cos(theta), r*np.sin(theta))


def main():
    # Implementeerige kõik nõutud operatsioonid kompleksarvudega siin:
    print("Kompleksarvude liitmine ja lahutamine: ", complex(1,3)-complex(-3, 7)-complex(-2, -2.4))
    print("Kompleksarvude liitmine ja lahutamine: ", complex(-1,4)+complex(1,2)+complex(4, 2)+complex(-4, 2))
    print("kompleksarvude korrutamine ja jagamine: ", (complex(6, 5)*complex(10, 8))/complex(10, -1))
    print("kompleksarvude korrutamine ja jagamine: ", (complex(-7, -7)/complex(-5, 8))*complex(-11, -8))
    print("Teisendamine eksponentkujule: ", algebraic_to_exponent(complex(3, 4)))
    print("Teisendamine eksponentkujule: ", algebraic_to_exponent(complex(-3, 4)))
    print("Eksponentkujul korrutamine: ", exponent_mult(3.0, np.pi/2, 2.5, -np.pi/3.0))
    print("Teisendamine algebralisele kujule: ", exponent_to_algebraic(3, (9*np.pi)/15))
    pass


if __name__ == "__main__":
    main()
