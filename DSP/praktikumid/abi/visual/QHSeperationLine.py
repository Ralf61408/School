from PyQt5.QtWidgets import QFrame, QSizePolicy

class QHSeperationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        #self.setProperty("qssClass", "qh_separation_line")
        return
