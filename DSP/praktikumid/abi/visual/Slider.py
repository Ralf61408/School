from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget

class Slider(QWidget):
    def __init__(self, minimum, maximum, parent=None, label_text="notext", start_value=0, scaler=1, tracking=True):
        super(Slider, self).__init__(parent=parent)
        self.verticalLayout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label_text = label_text
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout()

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(start_value)
        self.slider.setProperty("qssClass", "sliders")
        self.slider.setTracking(tracking)
        self.horizontalLayout.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.slider.valueChanged.connect(self.setLabelValue)
        self.x = None
        self.scaler = scaler
        self.setLabelValue(self.slider.value())

    def setLabelValue(self, value):
        self.x = value*self.scaler
        self.label.setText(self.label_text + ": {0:.4g}".format(self.x))
