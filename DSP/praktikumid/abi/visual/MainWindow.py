from PyQt5.QtWidgets import QWidget, QGridLayout

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.grid = QGridLayout(self)
