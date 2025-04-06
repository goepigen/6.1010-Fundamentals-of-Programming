# -*- coding: utf-8 -*-

# QApplication class is the core of every Qt Application: every application needs one
# and only one of such objects to function. This object holds the event loop.

# Each interaction generates an event, which is placed on the event queue.
# The queue is checked on each iteration of the event loop., and if an event is found
# the event and control is passed to the specific event handler for the event

# There is only one running event loop per application.

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6. QtCore import QSize, Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.button_is_checked = True
        # signals are notifications emitted by widgets when something happens
        # slots are receivers of signals (any function or method can be used as a slot, by
        # connecting the signal to it
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.setChecked(self.button_is_checked)
        # button.clicked.connect(self.the_button_was_clicked)
        self.button.clicked.connect(self.the_button_was_toggled)
        self.button.released.connect(self.the_button_was_released)

        self.setCentralWidget(self.button)

        # fixed size window that can't be resized
        self.setFixedSize(QSize(400, 300))
        # self.setMinimumSize()
        # self.setMaximumSize()

    def the_button_was_clicked(self):
        print("Clicked")

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()
        print(self.button_is_checked)


app = QApplication(sys.argv)

# All top-level widgets are windows - they don't have a parent and are not nested
# within another widget or layout. Technically we can create a window using any widget.

# window = QWidget()

window = MainWindow()

window.show()

app.exec()

# A widget is the name given to a component of the UI that the user can interact with.
