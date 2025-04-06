import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize


class _Bar(QtWidgets.QWidget):

    clickedValue = QtCore.pyqtSignal(int)

    def __init__(self, steps):
        super().__init__()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding
        )

        if isinstance(steps, list):
            self.n_steps = len(steps)
            self.steps = steps
        elif isinstance(steps, int):
            self.n_steps = steps
            self.steps = ["red"] * steps
        else:
            raise TypeError("steps must be list or int")

        self._bar_solid_percent = 0.8
        self._background_color = QtGui.QColor("black")
        self._padding = 4

    def sizeHint(self):
        return QtCore.QSize(40, 120)

    # PaintEvent handler is the core of all widget drawing in PyQt6. Every complete and partial
    # redraw of a widget is triggered through a painEvent which the widget handles to draw itself
    # When a paintEvent is triggered, your widget is able to redraw it.
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(
            0,
            0,
            painter.device().width(),
            painter.device().height(),
        )
        painter.fillRect(rect, brush)

        # get current state
        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        value = parent.value()

        pc = (value - vmin) / (vmax - vmin)
        n_steps_to_draw = int(pc * self.n_steps)

        padding = 5

        # active canvas area
        d_height = painter.device().height() - padding*2
        d_width = painter.device().width() - padding*2
        step_size = d_height/self.n_steps
        bar_height = step_size*0.6

        for n in range(n_steps_to_draw):
            brush.setColor(QtGui.QColor(self.steps[n]))
            ypos = (1+n)*step_size
            rect = QtCore.QRect(
                padding,
                padding + d_height - int(ypos),
                d_width,
                int(bar_height),
            )
            painter.fillRect(rect, brush)

        painter.end()

    def _calculate_clicked_value(self, e):
        parent = self.parent()
        vmin, vmax = parent.minimum(), parent.maximum()
        d_height = self.size().height() + (self._padding * 2)
        step_size = d_height / self.n_steps
        print(e)
        click_y = e.y() - self._padding - step_size / 2

        pc = (d_height - click_y) / d_height
        value = int(vmin + pc * (vmax - vmin))
        self.clickedValue.emit(value)

    def mouseMoveEvent(self, e):
        self._calculate_clicked_value(e)

    def mousePressEvent(self, e):
        self._calculate_clicked_value(e)

    def _trigger_refresh(self):
        self.update()


# any widget without a parent is a window
# thus, here we don't use QMainWindow
class PowerBar(QtWidgets.QWidget):
    def __init__(self, parent=None, steps=10):
        super().__init__(parent)
        # self.setFixedSize(QSize(400, 300))
        layout = QtWidgets.QVBoxLayout()

        # holds a _Bar
        self._bar = _Bar(steps)
        layout.addWidget(self._bar)

        # and a QDial
        self._dial = QtWidgets.QDial()
        self._dial.setNotchesVisible(True)
        self._dial.setWrapping(False)
        self._dial.valueChanged.connect(self._bar._trigger_refresh)

        self._bar.clickedValue.connect(self._dial.setValue)

        layout.addWidget(self._dial)
        self.setLayout(layout)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self[name]
        try:
            return getattr(self._dial, name)
        except AttributeError:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__, name))

    def setColor(self, color):
        self._bar.steps = [color] * self._bar.n_steps
        self._bar.update()

    def setColors(self, colors):
        self._bar.n_steps = len(colors)
        self._bar.steps = colors
        self._bar.update()

    def setBarPadding(self, i):
        self._bar._padding = int(i)
        self._bar.update()

    def setBarSolidPercent(self, f):
        self._bar._bar_solid_percent = float(f)
        self._bar.update()

    def setBackgroundColor(self, color):
        self._bar._background_color = QtGui.QColor(color)
        self._bar.update()


app = QtWidgets.QApplication(sys.argv)
bar = PowerBar(steps=["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598",
                      "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f", "#9e0142"])

bar.setBarPadding(2)
bar.setBarSolidPercent(0.9)
bar.setBackgroundColor('gray')
bar.show()
app.exec()
