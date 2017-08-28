import sys

from PyQt5 import QtWidgets, uic

Ui_MainWindow, MainWindowBase = uic.loadUiType('MainWindow.ui')

import numpy as np
from vispy import scene

from examples.gui.custom_plot_widget import CustomPlotWidget, LabelText


# using scene graph and custom PlotWidget
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

        x = np.linspace(0, 10, 100000)
        ytop = np.cos(x)
        ybottom = np.sin(x)

        top_chart = self.viewer._grid[0, 0]
        bottom_chart = self.viewer._grid[1, 0]
        ylabel_top = LabelText("y top", dim=30)
        ylabel_bottom = LabelText("y bottom", dim=30)
        xlabel = LabelText("x", dim=30)
        top_chart.configure(ylabel=ylabel_top)
        bottom_chart.configure(ylabel=ylabel_bottom, xlabel=xlabel)
        top_chart.plot((x, ytop))
        bottom_chart.plot((x, ybottom))

        # link viewbox cameras
        top_chart.view.camera.link(bottom_chart.view.camera)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
