import sys

from PyQt5 import QtWidgets, uic

Ui_MainWindow, MainWindowBase = uic.loadUiType('MainWindow.ui')

import numpy as np
from vispy import plot as vp

#using Fig in pyqt
class MainWindow(MainWindowBase):
    def __init__(self):
        MainWindowBase.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewer = vp.Fig()
        self.viewer.create_native()
        self.ui.plotFrameLayout.addWidget(self.viewer.native)

        x = np.linspace(0, 10, 100000)
        y = np.cos(x)

        self.viewer[0, 0].plot((x,y))
        grid1 = vp.visuals.GridLines(color=(0, 0, 0, 0.5))
        grid1.set_gl_state('translucent')
        self.viewer[0, 0].view.add(grid1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
