# -*- coding: utf-8 -*-

import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QComboBox,
    QListWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(400, 300))

        # Label
        defaultText = "New content: "
        self.label = QLabel(defaultText)
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # QCheckBox
        self.cb = QCheckBox("My Checkbox")
        self.cb.setCheckState(Qt.CheckState.Checked)
        self.cb.stateChanged.connect(self.show_state)

        # QComboBox - dropdown
        combo = QComboBox()
        combo.addItems([l for l in 'abcdefghijklmnopqrstuvwxyz'])
        combo.currentIndexChanged.connect(self.index_changed)
        combo.currentTextChanged.connect(self.text_changed)
        combo.setEditable(True)

        # QListWidget
        qList = QListWidget()
        qList.addItems([l for l in 'abcdefghijklmnopqrstuvwxyz'])
        qList.currentItemChanged.connect(self.qList_index_changed)
        qList.currentTextChanged.connect(self.qList_text_changed)

        # QLineEdit - Input
        self.input = QLineEdit()
        self.input.textChanged.connect(
            lambda text: self.label.setText(defaultText + text))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(combo)
        layout.addWidget(qList)
        layout.addWidget(self.cb)
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def show_state(self, s):
        print(Qt.CheckState(s) == Qt.CheckState.Checked)
        print(s)

    def index_changed(self, i):
        print(i)

    def text_changed(self, s):
        print(s)

    def qList_index_changed(self, i):
        print(i.text())

    def qList_text_changed(self, s):
        print(s)


app = QApplication(sys.argv)

# All top-level widgets are windows - they don't have a parent and are not nested
# within another widget or layout. Technically we can create a window using any widget.

# window = QWidget()

window = MainWindow()

window.show()

app.exec()


# Most widgets have their own signals.
