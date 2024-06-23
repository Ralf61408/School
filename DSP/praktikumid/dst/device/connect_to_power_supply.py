#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa

def power_supply_get_instrument() -> pyvisa.resources.Resource:
    rm = pyvisa.ResourceManager()

    # Järgneva käsuga saab loetleda kõik ühendatud seadmed. Hea viis ühenduse veaotsinguks.
    print(rm.list_resources())

    # Ühendume läbi USB signaaligeneraatori külge ja loome klassist vastava isendi.
    usb_resources = list(filter(lambda name: 'USB' in name and 'DP8C' in name, rm.list_resources()))
    return rm.open_resource(usb_resources[0])
