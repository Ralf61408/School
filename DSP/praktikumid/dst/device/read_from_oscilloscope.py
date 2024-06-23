#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa
import numpy as np
from time import sleep
from dst.device.decode_preamble import convert_waveform_preamble


def wait_until_ready_to_trigger(osc_inst):
    while(True):
        # Kui ostsilloskoop ootab sünkronisatsioonisignaali, on 'Trigger:Status' parameetri väärtus 'wait'
        val = osc_inst.query(':TRIGger:STATus?')
        print(val)
        if val == 'WAIT':
            break
        sleep(0.1)


def wait_until_measurement_done(osc_inst):
    while(True):
        # Kui teeme 'single' tüüpi mõõtmise, lõpetab ostsilloskoop soovitud andmemahu täitumisel
        # ise mõõtmise ja 'Trigger:Status' parameetri väärtuseks saab 'Stop'
        val = osc_inst.query(':TRIGger:STATus?')
        print(val)
        if val == 'STOP':
            break
        sleep(0.1)


def get_oscilloscope_data(ip_addr: str, channel: int, y_scale: float, y_offset: float):

    # Ühendume ostsilloskoobiga
    rm = pyvisa.ResourceManager()
    osc_inst = rm.open_resource('TCPIP::{ip_addr}::INSTR'.format(ip_addr=ip_addr), read_termination="\n", write_termination="\n")

    # Veendume, et ainult valitud kanal oleks aktiivne.
    osc_inst.write(':CHANnel1:DISPlay 0')
    osc_inst.write(':CHANnel2:DISPlay 0')
    osc_inst.write(':CHANnel3:DISPlay 0')
    osc_inst.write(':CHANnel4:DISPlay 0')
    osc_inst.write(f':CHANnel{channel}:DISPlay 1')

    # Määrame triggeri mõnele mittekasutatavale kanalile, et see ei segaks meie mõõtmist.
    osc_inst.write(f':TRIGger:EDGe:SOURce CHANnel{channel % 4 + 1}')

    # Määrame prooviku režiimiks 1x
    osc_inst.write(f':CHANnel1:PROBe 1')

    # Ostsilloskoobi mälu sügavust saab muuta ainult mittepeatatud olekus.
    osc_inst.write(':RUN')

    # Määrame ära, et soovime korraga hõivata 600 000 andmepunkti.
    osc_inst.write(':ACQuire:MDEPth 600000')

    # Seiskame ostsilloskoobi.
    osc_inst.write(':STOP')

    # Samuti kustutame eelnevate mõõtmiste andmed ostsilloskoobi mälust:
    osc_inst.write(':CLEar')

    # Seame ajalise jaotise suuruseks 500 ms, sedasi mõõdame kokku 12x0.5s = 6s
    # selle aja jooksul salvestatakse meie küsitud 600 000 andmepunkti.
    osc_inst.write(':TIMebase:MAIN:SCALe 0.5')

    # Määrame ajalise nihke nii, et mõõdame ainult sünkroniseerimispunktile (trigger) järgnevat osa.
    osc_inst.write(':TIMebase:MAIN:OFFSet 0.0')
    osc_inst.write(':TIMebase:OFFSet 3')  # Selleks peame nihutama 6 jaotist ehk 3 s

    # Leidke sobivad käsud, et määrata vastavalt parameetritele ostsilloskoobi vertikaalne jaotus ja nihe.
    osc_inst.write(f":CHANnel{channel}:SCALe {y_scale}V")
    osc_inst.write(f":CHANnel{channel}:OFFSet {y_offset}V")

    # Veendume, et ostsilloskoobil on piisavalt aega kõigi saadud käskude töötlemiseks.
    sleep(0.2)
    # Teeme eelnevalt määratud parameetritega ühe mõõtmise.
    osc_inst.write(':SINGle')

    # Kui ostsilloskoop on valmis, saadame ka käsitsi sünkroniseerimissignaali, vältimaks olukorda,
    # kus me ei alusta mõõtmist, kuna meie signaal ei ületa kunagi sünkroniseerimislävendit.
    wait_until_ready_to_trigger(osc_inst)
    osc_inst.write(':TFORce')

    # Ootame, et mõõtmine saaks tehtud ja ostsilloskoop oleks uuesti peatatud režiimis.
    wait_until_measurement_done(osc_inst)

    # Nüüd saame alustada andmete lugemist oma Python programmi.
    # Selleks esmalt määrame, mis kujul soovime andmeid saada.
    osc_inst.write(f':WAVeform:SOUR CHANnel1')  # Mis kanali infot loeme.
    osc_inst.write(':WAVeform:MODE RAW')  # Loeme mälust toorandmeid.
    osc_inst.write(':WAVeform:FORMat BYTE')  # Andmed küsime byte kujul (8-bitine resolutsioon).

    # Korraga saame lugeda maksimaalselt 250 000 andmepunkti, seega teostame 600 000 punkti lugemise kolmes osas.
    osc_inst.write(':WAVeform:START 1')  # Andmete lugemise algusindeks seadme mälus.
    osc_inst.write(':WAVeform:STOP 200000')  # Andmete lugemise lõppindeks seadme mälus.
    # Järgnev käsk teostab andmete lugemise.
    waveform_datapoints1 = osc_inst.query_binary_values(':WAVeform:DATA?', datatype="B", container=np.array).astype(np.float32)

    # kordame sama järgmiste osade jaoks.
    osc_inst.write(':WAVeform:START 200001')
    osc_inst.write(':WAVeform:STOP 400000')
    waveform_datapoints2 = osc_inst.query_binary_values(':WAVeform:DATA?', datatype="B", container=np.array).astype(np.float32)
    osc_inst.write(':WAVeform:START 400001')
    osc_inst.write(':WAVeform:STOP 600000')
    waveform_datapoints3 = osc_inst.query_binary_values(':WAVeform:DATA?', datatype="B", container=np.array).astype(np.float32)

    # Ühendame andmed üheks tervikuks.
    waveform_datapoints = np.concatenate((waveform_datapoints1, waveform_datapoints2, waveform_datapoints3))

    # Küsime mõõteriistalt mõõtmisel kasutatud parameetrid ja teisendame need lihtsasti kasutavaks sõnastikuks
    preamble_dict = convert_waveform_preamble(osc_inst.query(":WAVeform:PREamble?"))

    osc_inst.close()

    return waveform_datapoints, preamble_dict


if __name__ == '__main__':
    pass
