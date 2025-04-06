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
from random import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on Earth',
    'What on Earth',
    'Something Went Wrong'
]


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
        self.button.clicked.connect(self.the_button_was_clicked)
        self.windowTitleChanged.connect(self.the_window_title_changed)

        self.setCentralWidget(self.button)

        # fixed size window that can't be resized
        self.setFixedSize(QSize(400, 300))
        # self.setMinimumSize()
        # self.setMaximumSize()

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something Went Wrong':
            self.button.setDisabled(True)

    def the_button_was_clicked(self):
        # self.button.setText("You already clicked me")
        # self.button.setEnabled(False)

        new_window_title = choice(window_titles)
        print("Setting title: %s" % new_window_title)
        self.setWindowTitle(new_window_title)


app = QApplication(sys.argv)

# All top-level widgets are windows - they don't have a parent and are not nested
# within another widget or layout. Technically we can create a window using any widget.

# window = QWidget()

window = MainWindow()

window.show()

app.exec()


# Most widgets have their own signals.
