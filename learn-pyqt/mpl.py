# -*- coding: utf-8 -*-
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox
)

import os

matplotlib.use("QtAgg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(121)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        self.setCentralWidget(sc)

        self.show()


app = QApplication(sys.argv)

# All top-level widgets are windows - they don't have a parent and are not nested
# within another widget or layout. Technically we can create a window using any widget.

# window = QWidget()

window = MainWindow()

# window.show()

app.exec()


# Most widgets have their own signals.

class SingleAnimation(QWidget):
    
    def __init(self, parent):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        
        combo = QComboBox()
        
        path = "/Users/marcusegues/maple/Packages/QComputing/csv"
        
        entries = os.scandir(path)
        
        files = [entry for entry in entries if entry.is_file()]
        
        combo.addItems(files)
        combo.currentIndexChanged.connect(self.index_changed)
        combo.currentTextChanged.connect(self.text_changed)
        
        layout.addWidget(combo)
        

def getCsvFiles(path):
    dirFiles = os.listdir(path)
    
    