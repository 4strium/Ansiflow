import json
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize

class GridWidget(QWidget):
    def __init__(self, map_size, border_color, wall_color, player_color, parent=None):
        super().__init__(parent)
        self.map_size = map_size
        self.border_color = QColor(border_color)
        self.wall_color = QColor(wall_color)
        self.player_color = QColor(player_color)
        self.cells = [[0]*map_size for _ in range(map_size)]
        self.pos_player = [-1,-1]
        self.pos_enemies = []
        self.map_mode = 0
        self.filename = "workingDir/data.json"
        self.setMouseTracking(True)
    
    def setMap_mode(self, nmode):
        self.map_mode = nmode

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
                if [i,j] == self.pos_player :
                    painter.fillRect(x, y, sz, sz, QColor(self.player_color))
                else :
                    painter.fillRect(x, y, sz, sz, self.wall_color if self.cells[i][j] else QColor("#EBEBEB"))
                painter.setPen(self.border_color)
                painter.drawRect(x, y, sz-1, sz-1)

    def initJsonGrid(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
                data["map"] = [[0]*self.map_size for _ in range(self.map_size)]
        self.cells = data["map"]
        
        self.update()
        

    def mousePressEvent(self, event):
        pos = event.position()       

        x, y = pos.x(), pos.y()

        w, h = self.width(), self.height()
        sz = min(w // self.map_size, h // self.map_size)
        x_off = (w - sz * self.map_size) // 2
        y_off = (h - sz * self.map_size) // 2

        j = int((x - x_off) // sz)
        i = int((y - y_off) // sz)
        if 1 <= i < self.map_size -1 and 1 <= j < self.map_size -1 and self.map_mode != 0:
            if self.filename:
                try:
                    with open(self.filename, "r") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                        data["map"] = [[0]*self.map_size for _ in range(self.map_size)]
                if data["map"][i][j] and self.map_mode == 2  : 
                    data["map"][i][j] = not data["map"][i][j]
                elif not data["map"][i][j] and self.map_mode == 1 and [i,j] != self.pos_player :
                    data["map"][i][j] = not data["map"][i][j]
                elif self.map_mode == 3 and not data["map"][i][j]:
                    self.pos_player = [i, j]
                with open(self.filename, "w") as f:
                    json.dump(data, f)
                self.cells = data["map"]
                self.update()