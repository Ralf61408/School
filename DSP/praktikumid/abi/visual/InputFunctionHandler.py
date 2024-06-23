from abi.visual.ComponentView import ComponentView

class InputFunctionHandler():
    def __init__(self) -> None:
        self.freq_func = lambda x, y: 0
        self.freq_converter = lambda x: 0

    def set_component_function(self, func):
        for comp in ComponentView.sum_components:
            comp.f_x = func
            comp.update_plot()
        ComponentView.update_components_sum()

    def set_compare_function(self, func):
        for comp in ComponentView.sum_components:
            comp.f_compare = func
            comp.update_plot()
        ComponentView.update_components_sum()

    def set_sum_function(self, sum_func):
        ComponentView.sum_func = sum_func

    def set_frequency_finder(self, freq_func):
        self.freq_func=freq_func

    def set_frequency_converter(self, freq_converter):
        self.freq_converter=freq_converter
