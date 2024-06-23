#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa
from time import sleep

def main():
    # Ühendume ostsilloskoobiga kohalikult määratud hosti nime alusel
    rm = pyvisa.ResourceManager()
    # NB! Sisesta oma ostsilloskoobi IP!
    osc_inst = rm.open_resource('TCPIP::172.17.55.20::INSTR', read_termination="\n", write_termination="\n")

    # Saadame ostsilloskoobile seadete algväärtustamise käsu.
    osc_inst.write('*RST')
    # Kuna reset võtab aega, ootame natuke.
    sleep(10)
    # Sulgeme ühenduse.
    osc_inst.close()

if __name__ == '__main__':
    main()
