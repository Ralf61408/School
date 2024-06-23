#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa

def signal_generator_get_instrument() -> pyvisa.resources.Resource:
    """
    Funktsioon, mis tagastab PyVISA signaaligeneraatori ressursi objekti.
    Tagastab:
        signaaligeneraatori ressursi objekt.
    """
    rm = pyvisa.ResourceManager()

    # Järgneva käsuga saab loetleda kõik ühendatud seadmed. Hea viis ühenduse veaotsinguks.
    # print(rm.list_resources())

    # Ühendume läbi USB signaaligeneraatori külge ja loome klassist vastava isendi.
    usb_resources = list(filter(lambda name: 'USB' in name and 'DG8A' in name, rm.list_resources()))
    return rm.open_resource(usb_resources[0])
