from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize

class GridWidget(QWidget):
    def __init__(self, map_size, border_color, checked_bg_color, parent=None):
        super().__init__(parent)
        self.map_size = map_size
        self.border_color = QColor(border_color)
        self.checked_bg_color = QColor(checked_bg_color)
        self.cells = [[False]*map_size for _ in range(map_size)]
        self.setMouseTracking(True)

    def sizeHint(self):
        return QSize(400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        sz = min(w//self.map_size, h//self.map_size)
        x_off = (w - sz*self.map_size)//2
        y_off = (h - sz*self.map_size)//2

        for i in range(self.map_size):
            for j in range(self.map_size):
                x = x_off + j*sz
                y = y_off + i*sz
                painter.fillRect(x, y, sz, sz, self.checked_bg_color if self.cells[i][j] else QColor("#EBEBEB"))
                painter.setPen(self.border_color)
                painter.drawRect(x, y, sz-1, sz-1)

    def mousePressEvent(self, event):
        pos = event.position()       

        x, y = pos.x(), pos.y()

        w, h = self.width(), self.height()
        sz = min(w // self.map_size, h // self.map_size)
        x_off = (w - sz * self.map_size) // 2
        y_off = (h - sz * self.map_size) // 2

        j = int((x - x_off) // sz)
        i = int((y - y_off) // sz)
        if 0 <= i < self.map_size and 0 <= j < self.map_size:
            self.cells[i][j] = not self.cells[i][j]
            self.update()