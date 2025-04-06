import sys

from PyQt6.QtWidgets import QApplication, QWidget


class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        # defines location of the window on the screen and dimensions
        # (x, y, width, height)
        self.setGeometry(200, 600, 400, 300)
        self.setWindowTitle("Empty Window in PyQt")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmptyWindow()
    sys.exit(app.exec())


# minimal example
# import sys     # used to access command line arguments
# from PyQt6.QtWidgets import QApplication, QWidget

# app = QApplication(sys.argv)
# window = QWidget()
# window.show()
# sys.exit(app.exec())
