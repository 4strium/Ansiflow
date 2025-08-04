import json, math
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QPainter, QColor, QMouseEvent
from PyQt6.QtCore import QSize

class GridWidget(QWidget):
  def __init__(self, main_app, map_size, border_color, wall_color, player_color, enemy_color, enemy_path, parent=None):
    super().__init__(parent)
    self.mainApp = main_app
    self.map_size = map_size
    self.border_color = QColor(border_color)
    self.wall_color = QColor(wall_color)
    self.player_color = QColor(player_color)
    self.enemy_color = QColor(enemy_color)
    self.exit_color = QColor("#ff00dd")
    self.cells = [[0]*map_size for _ in range(map_size)]
    self.pos_player = []
    self.pos_enemies = []
    self.pos_NPCS = []
    self.pos_exit = []
    self.enemy_img = enemy_path
    self.map_mode = 0
    self.filename = "workingDir/data.json"
    self.pers_pos_attribution = main_app.pos_given
    self.congestion_limit = 4
    self.setMouseTracking(True)
  
  def setMap_mode(self, nmode):
    self.map_mode = nmode

  def setEnemyImg(self, path):
    self.enemy_img = path
    with open(self.filename, "r") as f:
      data = json.load(f)
    with open(self.filename, "w") as f:
      data["Enemy"] = self.packEnemies()
      json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)

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
          painter.fillRect(x, y, sz, sz, self.player_color)
        elif [i,j] in self.pos_enemies :
          painter.fillRect(x, y, sz, sz, self.enemy_color)
        elif [i,j] in [npc[0] for npc in self.pos_NPCS]:
          npc_color = [npc[1] for npc in self.pos_NPCS if npc[0] == [i, j]][0]
          painter.fillRect(x, y, sz, sz, QColor(npc_color))
        elif [i,j] == self.pos_exit :
          painter.fillRect(x, y, sz, sz, self.exit_color)
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
    self.pos_player = [coord - 0.5 for coord in data["player"]]
    for element in data["Enemy"] :
      self.pos_enemies.append([int(coord - 0.5) for coord in element["position"] ])  
    self.pos_exit = data["exit"]    
    self.update()
      
  def checkNearestEnemy(self, position_given):
    all_pos = []
    for pos in self.pos_enemies :
      dist = math.sqrt((pos[0] - position_given[0])**2 + (pos[1] - position_given[1])**2)
      all_pos.append(dist)
    if len(all_pos) :
      return min(all_pos)
    return math.inf
  
  def checkNearestNPC(self, position_given, pass_name=""):
    all_pos = []
    for pos in self.pos_NPCS :
      if pos[2] != pass_name :
        dist = math.sqrt((pos[0][0] - position_given[0])**2 + (pos[0][1] - position_given[1])**2)
        all_pos.append(dist)
    if len(all_pos) :
      return min(all_pos)
    return math.inf
      
  def packEnemies(self):
    package = []
    for position in self.pos_enemies :
      individual_dict = {}
      individual_dict["position"] = [coord + 0.5 for coord in position]
      individual_dict["path_visual"] = self.enemy_img
      package.append(individual_dict)
    return package

  def mousePressEvent(self, event):
    pos = event.position()       

    x, y = pos.x(), pos.y()

    w, h = self.width(), self.height()
    sz = min(w // self.map_size, h // self.map_size)
    x_off = (w - sz * self.map_size) // 2
    y_off = (h - sz * self.map_size) // 2

    j = int((x - x_off) // sz)
    i = int((y - y_off) // sz)
    if self.filename:
      try:
        with open(self.filename, "r") as f:
          data = json.load(f)
      except (FileNotFoundError, json.JSONDecodeError):
        data["map"] = [[0]*self.map_size for _ in range(self.map_size)]
      if 1 <= i < self.map_size -1 and 1 <= j < self.map_size -1 and self.map_mode != 0:
        if data["map"][i][j] and self.map_mode == 2  : 
          data["map"][i][j] = not data["map"][i][j]
        elif not data["map"][i][j] and self.map_mode == 1 and [i,j] != self.pos_player and [i,j] not in self.pos_enemies :
          data["map"][i][j] = not data["map"][i][j]
        elif self.map_mode == 3 and not data["map"][i][j] and [i,j] not in self.pos_enemies :
          if self.pos_player != [i, j] :
            self.pos_player = [i, j]
            data["player"] = [i+0.5, j+0.5]
          else :
            self.pos_player = [-1, -1]
            data["player"] = [-1, -1]
        elif self.map_mode == 4 and not data["map"][i][j] and [i,j] != self.pos_player :
          if [i,j] not in self.pos_enemies :
            if self.checkNearestNPC([i,j]) > self.congestion_limit :
              if self.checkNearestEnemy([i,j]) > self.congestion_limit :
                self.pos_enemies.append([i,j])
              else :
                QMessageBox.warning(self, "Ennemis trop proches", "Vous ne pouvez malheureusement pas placer un ennemi ici, car il serait trop proche d'un de ses congénères.")
            else :
              QMessageBox.warning(self, "Personnage trop proche", "Vous ne pouvez malheureusement pas placer un ennemi ici, car il serait trop proche d'un personnage.") 
          else :
            self.pos_enemies.remove([i,j])
        elif self.map_mode == 5 and not data["map"][i][j] and [i,j] not in self.pos_enemies and [i,j] != self.pos_player:
          npc_select = self.mainApp.current_NPC_selected
          if self.checkNearestEnemy([i,j]) > self.congestion_limit :
            if self.checkNearestNPC([i,j], npc_select) > self.congestion_limit :
              if npc_select :
                for npc in self.mainApp.NPCs :
                  if npc[0] == npc_select :
                    attributed_color = npc[1]
                    self.pos_NPCS = [npc for npc in self.pos_NPCS if npc[1] != attributed_color]
                self.pos_NPCS.append([[i,j], attributed_color, npc_select])
                self.pers_pos_attribution([i, j])
            else :
              QMessageBox.warning(self, "Personnages trop proches", "Vous ne pouvez malheureusement pas placer un personnage ici, car il serait trop proche d'un de ses congénères.") 
          else :
            QMessageBox.warning(self, "Ennemi trop proche", "Vous ne pouvez malheureusement pas placer un personnage ici, car il serait trop proche d'un ennemi.")
      elif ((i == 0 ) or (j == 0) or (i == self.map_size-1) or (j == self.map_size-1)) and [i,j] not in [[0,0],[0,self.map_size-1],[self.map_size-1,0],[self.map_size-1,self.map_size-1]] and (self.map_mode == 6) :
        self.pos_exit = [i,j]
        data["exit"] = [i,j]
      with open(self.filename, "w") as f:
        data["Enemy"] = self.packEnemies()
        json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)
      self.cells = data["map"]
      self.update()