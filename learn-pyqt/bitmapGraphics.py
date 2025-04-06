# To create custom widgets we need to understand  bitmap (pixel-based) graphic operations
# All standard widgets draw themselves as bitmaps on a rectangular "canvas" that forms the
# shape of the widget.
# Bitmap: rectangular grid of pixels

# Bitmap drawing operations in Qt handled through the QPainter class

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # QLabel can display images, and is the simplest widget available for displaying a QPixmap
        self.label = QLabel()

        # QPixmap we will draw on
        self.canvas = QPixmap(400, 300)
        # We fill the canvas with an initial color because the default depends on the platform
        self.canvas.fill(Qt.GlobalColor.white)
        # self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        painter = QPainter(self.canvas)
        painter.drawLine(10, 10, 300, 200)
        painter.end()
        self.label.setPixmap(self.canvas)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
