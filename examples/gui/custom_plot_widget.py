from vispy import scene, plot
import numpy as np

class LabelText:
    def __init__(self, text="", font_size=12, color="k", dim=40):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.dim = dim

class CustomPlotWidget(scene.Widget):
    def __init__(self, *args, **kwargs):
        self.grid = None
        self.section_y_x = None
        super(CustomPlotWidget, self).__init__(*args, **kwargs)
        self.grid = self.add_grid(spacing=0, margin=10)

    def configure(self, xlabel=None, ylabel=None):
        self.unfreeze()
        self._setup_view()
        if ylabel is not None:
            self._setup_yaxis(ylabel)
            self.yaxis.link_view(self.view)
        if xlabel is not None:
            self._setup_xaxis(xlabel)
            self.xaxis.link_view(self.view)
        self.freeze()

    def plot(self, data, color='k', width=1.0, kind="line"):
        obj = None
        if kind == "line":
            obj = self._plot_line(color, data, width)
        if kind =="candle_stick":
            obj = self._plot_candle_sticks(data)
        return obj

    def _plot_line(self, color, data, width):
        line = scene.LinePlot(data, connect='strip', color=color, width=width)
        self.view.add(line)
        self.view.camera.set_range()
        return line

    def _plot_candle_sticks(self, data_list):
        i = 0
        n = len(data_list)
        for data in data_list:
            print(i,"of", n)
            self._plot_candle_stick(data)
            i+=1
        self.view.camera.set_range()

    def _plot_candle_stick(self, data):
        time = data["time"]
        open = data["open"]
        high = data["high"]
        low = data["low"]
        close = data["close"]

        width = data["time_frame"] * 0.8

        bullish = close > open
        height = abs(open - close)
        center = (time, open + height * 0.5 if bullish else open - height * 0.5)
        rect = None
        if height > 0:
            rect = scene.Rectangle(center=center, height=height, width=width, color = "green" if bullish else "red",
                                   border_color="black", border_width=2.0)
            self.view.add(rect)
        else:
            line_empty_body = scene.Line(pos=np.array([[time - width*0.5, close], [time + width*0.5, close]]), color="black", width=2.0)
            self.view.add(line_empty_body)
        line_high = scene.Line(pos=np.array([[time, close if bullish else open], [time, high]]), color="black", width=2.0)
        line_low = scene.Line(pos=np.array([[time, open if bullish else close], [time, low]]), color="black", width=2.0)
        self.view.add(line_high)
        self.view.add(line_low)
        return rect if rect is not None else line_empty_body

    def _setup_yaxis(self, ylabel):
        self.ylabel = scene.Label(ylabel.text, font_size=ylabel.font_size, color=ylabel.color, rotation=-90)
        ylabel_widget = self.grid.add_widget(self.ylabel, row=0, col=0)
        ylabel_widget.width_max = ylabel.dim
        self.yaxis = scene.AxisWidget(orientation='left', text_color=ylabel.color, axis_color=ylabel.color, tick_color=ylabel.color, )
        yaxis_widget = self.grid.add_widget(self.yaxis, row=0, col=1)
        yaxis_widget.width_max = ylabel.dim

    def _setup_xaxis(self, xlabel):
        self.xaxis = scene.AxisWidget(orientation='bottom', text_color=xlabel.color, axis_color=xlabel.color, tick_color=xlabel.color)
        xaxis_widget = self.grid.add_widget(self.xaxis, row=1, col=2)
        xaxis_widget.height_max = xlabel.dim
        self.xlabel = scene.Label(xlabel.text, font_size=xlabel.font_size, color=xlabel.color)
        xlabel_widget = self.grid.add_widget(self.xlabel, row=2, col=2)
        xlabel_widget.height_max = xlabel.dim

    def _setup_view(self):
        self.view = self.grid.add_view(row=0, col=2, border_color='grey', bgcolor="#efefef")
        self.view.camera = 'panzoom'
        grid_lines = plot.visuals.GridLines(color=(0, 0, 0, 0.5))
        grid_lines.set_gl_state()
        self.view.add(grid_lines)