import sys
import os

from PyQt5 import QtWidgets, uic

Ui_MainWindow, MainWindowBase = uic.loadUiType('MainWindow.ui')

import numpy as np
from vispy import scene
from examples.gui.custom_plot_widget import CustomPlotWidget, LabelText

from vispy.color import Color

# candle stick chart with visuals
class MainWindow(MainWindowBase):
    def __init__(self):
        MainWindowBase.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewer = scene.SceneCanvas(bgcolor='w')
        self.viewer.create_native()
        self.ui.plotFrameLayout.addWidget(self.viewer.native)
        self.viewer.unfreeze()
        self.viewer._grid = self.viewer.central_widget.add_grid()
        self.viewer._grid._default_class = CustomPlotWidget
        self.viewer.freeze()
        self.viewer.measure_fps()

        self.selected_candle = None
        self.base_color = None
        self.viewer.connect(self.on_mouse_press)

        self.chart = self.viewer._grid[0, 0]
        ylabel= LabelText("y", dim=30)
        xlabel = LabelText("x", dim=30)
        self.chart.configure(ylabel=ylabel, xlabel=xlabel)
        path = os.path.sep.join(["C:", "fxdata", "Candlesticks.csv"])
        data_points = np.genfromtxt(path, skip_header=1, delimiter=",")
        data_list = []
        for i in range(10):
            data_list.append({
                "time": i,
                "open": data_points[i, 1],
                "high": data_points[i, 2],
                "low": data_points[i, 3],
                "close": data_points[i, 4],
                "time_frame": 1
            })

        self.chart.plot(data_list, kind="candle_stick")

    def on_mouse_press(self, event):
        if event.handled or event.button != 1:
            return
        if self.selected_candle is not None:
            self.selected_candle._color = self.base_color
            self.selected_candle._update()
            self.selected_candle = None
            return
        for v in self.viewer.visuals_at(event.pos):
            if isinstance(v, scene.visuals.Rectangle):
                self.selected_candle = v
                break
        if self.selected_candle is not None:
            self.base_color = self.selected_candle._color
            self.selected_candle._color = Color("y")
            self.selected_candle._update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
