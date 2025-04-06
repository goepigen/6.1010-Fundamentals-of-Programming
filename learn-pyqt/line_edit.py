# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.label = QLabel()
        self.input = QLineEdit()

        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)

# All top-level widgets are windows - they don't have a parent and are not nested
# within another widget or layout. Technically we can create a window using any widget.

# window = QWidget()

window = MainWindow()

window.show()

app.exec()


# Most widgets have their own signals.
