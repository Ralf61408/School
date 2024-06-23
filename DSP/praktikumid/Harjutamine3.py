# 3. yl 10 praks, fft, 8 praks. teen monoks, see normaliseerimine. siis see valem telos, np.linspace see signaal (0,1, 44100)

# 1. yl 1 - 4, 9 praks

# 2. yl 7, 8 prax 

#3.yl
#def sumbuvfilter(sisend, slambda)

#def sabloon(threshold, sisend1, sisend2)
#    while


#np.linspace see signaal (0,1, 44100)

#slambda = 5
#out = sumbuvfilter(x, lambda)
#win.pg.graph


import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

def sumbuvfilter(sisend, slambda):
    """
    Sumbuvusfiltri rakendamine sisendsignaalile.
    """
    out = np.exp(-slambda * np.pi * sisend)
    return out

def sabloon(threshold, sisend1, sisend2):
    """
    Rakendab künnise alusel väärtusi sisend2-st sisend1-le.
    """
    out = np.copy(sisend1)
    for i in range(len(sisend1)):
        if sisend2[i] > threshold:
            out[i] = sisend2[i]
    return out

# Generaator lineaarse signaali loomiseks
x = np.linspace(0, 1, 44100)

# Rakendame sumbuvusfiltrit signaalile
slambda = 5
out = sumbuvfilter(x, slambda)

# Graafiku seadistamine ja kuvamine
def plot_signal():
    app = QtWidgets.QApplication([])
    win = pg.GraphicsLayoutWidget(show=True, title="Filtered Signal")
    plot = win.addPlot(title="Sumbuvfilter ja sabloon")
    
    plot.setLabel('left', 'Amplitude')
    plot.setLabel('bottom', 'Sample')
    
    plot.plot(x, pen='b', name="Originaal Signaal")
    plot.plot(out, pen='r', name="Sumbuvfilter")
    
    threshold = 0.5
    sisend2 = np.sin(2 * np.pi * 5 * x)  # Näide teise signaali genereerimiseks
    out2 = sabloon(threshold, out, sisend2)
    
    plot.plot(out2, pen='g', name="Sabloon")
    
    QtWidgets.QApplication.instance().exec_()

if __name__ == "__main__":
    plot_signal()

