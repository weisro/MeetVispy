import sys

from PyQt5 import QtGui, QtCore, QtWidgets, uic

Ui_MainWindow, MainWindowBase = uic.loadUiType('MainWindow.ui')

import numpy as np
from vispy import scene

from examples.gui.custom_plot_widget import CustomPlotWidget, LabelText

n_size = 10000
x = np.linspace(0, 100, n_size)

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

        self.selected_line = None
        self.viewer.connect(self.on_mouse_press)
        self.viewer.connect(self.on_mouse_move)

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
                line.interactive = True
                self.line_plots[key] = line
            else:
                self.line_plots[key].visible = True
        else:
            if key in self.line_plots:
                self.line_plots[key].visible = False

    def on_mouse_press(self, event):
        if event.handled or event.button != 1:
            return
        if self.selected_line is not None:
            self.selected_line.set_data(color="k")
            self.selected_line = None
            return
        for v in self.viewer.visuals_at(event.pos):
            if isinstance(v, scene.visuals.LinePlot):
                self.selected_line = v
                break
        if self.selected_line is not None:
            self.selected_line.set_data(color="r")

    def on_mouse_move(self, event):
        if self.selected_line is None:
            self.ui.statusbar.showMessage("")
            return
        tr = self.viewer.scene.node_transform(self.selected_line)
        pos = tr.map(event.pos)
        text = "x=%0.2f ms, y=%0.2f " % (pos[0], pos[1])
        self.ui.statusbar.showMessage(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
