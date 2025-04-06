# -*- coding: utf-8 -*-
import sys
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout

# custom widget
class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        
        layout = QVBoxLayout()
        layout.addWidget(Color("red"))
        layout.addWidget(Color("green"))
        layout.addWidget(Color("blue"))
        
        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()


