import sys

from PyQt5 import QtGui, QtCore, QtWidgets, uic

Ui_MainWindow, MainWindowBase = uic.loadUiType('MainWindow.ui')

import numpy as np
from vispy import scene

from examples.gui.custom_plot_widget import CustomPlotWidget, LabelText

n_size = 1000000
x = np.linspace(0, 50, n_size)

data_model = {
    "dataset a": {
        "x": x,
        "y": np.sin(x)
    },
    "dataset b": {
        "x": x,
        "y": np.cos(x)
    }
}

# control plot visibility with checkboxes
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

        self.chart = self.viewer._grid[0, 0]
        self.chart.configure(ylabel=LabelText("Y-Axis", dim=30), xlabel=LabelText("X-Axis", dim=30))

        self.line_plots = {}

        self.list_view_model = QtGui.QStandardItemModel()

        for key in data_model.keys():
            item = QtGui.QStandardItem(key)
            item.setCheckable(True)
            item.setEditable(False)
            self.list_view_model.appendRow(item)

        self.ui.listView.setModel(self.list_view_model)

        self.list_view_model.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        key = item.text()
        if item.checkState() == QtCore.Qt.Checked:
            if key not in self.line_plots:
                line = self.chart.plot((data_model[key]["x"], data_model[key]["y"]))
                self.line_plots[key] = line
            else:
                self.line_plots[key].visible = True
        else:
            if key in self.line_plots:
                self.line_plots[key].visible = False



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
