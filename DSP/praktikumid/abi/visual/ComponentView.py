from abi.visual.SliderPlot import SliderPlot
import numpy as np

class ComponentView(SliderPlot):
    sum_components = []
    sum_func = lambda signals: signals[0] # Vaikimisi võtab lihtsalt esimese massiivi
    combo_plot = None

    def __init__(self, grid, row, x_values, parent=None, sum_comp=False, plot_title = "No name plot", plot_name=None, yRange=(-20,20), hide_sliders=[], label="Magnituud:"):
        self.frequency = 1
        self.scaler = 1
        self.phase = 0
        self.f_x = lambda a,b,c,d : a
        self.f_compare = lambda a,b : 0
        self.data = 0

        self.sum_comp = sum_comp
        if sum_comp: #kohtle seda komponenti kui summa osa teistega
            self.add_sum_component(self)

        super().__init__(grid, row, x_values, parent=parent, plot_title=plot_title, plot_name=plot_name, yRange=yRange, label=label)
        self.hide_sliders(hide_sliders)

    def update_plot(self):
        self.frequency, self.scaler, self.phase, *_ = [s.x for s in self.sliders]
        self.phase *= np.pi/180

        self.data = self.f_x(self.x, self.frequency, self.scaler, self.phase)
        self.curve.setData(self.data)

        if self.sum_comp:
            self.update_components_sum()

        scalarProduct = self.f_compare(self.data, ComponentView.combo_plot.orig_data)
        if scalarProduct is not None:
            float_format = ".3f" if abs(scalarProduct)>0.01 else ".2e" #Vali vastavalt suurusjärgule eksponent või fix-koma kuju
            self.label.setText(("Skalaar-\nkorrutis:\n{0:10"+float_format+"}").format(scalarProduct))
        else:
            self.label.hide()

    @classmethod
    def add_sum_component(cls, component):
        cls.sum_components.append(component)

    @classmethod
    def update_components_sum(cls):
        if len(cls.sum_components):
            data = cls.sum_func([comp.data for comp in cls.sum_components])
            cls.combo_plot.update_sum_plot(data)

    def init_sliders(self):
        self.add_slider(0, self.x.shape[0], self.update_plot, label_text="Sagedus [k]")
        self.add_slider(0, 20, self.update_plot, label_text="Amplituud [a]", start_value=1)
        self.add_slider(0, 360, self.update_plot, label_text="Faasinihe [φ]")

    def hide_slider(self, index):
        self.sliders[index].hide()

    def hide_sliders(self, indexes):
        for i in indexes:
            self.hide_slider(i)
