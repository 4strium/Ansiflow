import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QTextEdit
from PyQt6.QtGui import QFont, QFontMetrics, QKeyEvent
from PyQt6.QtCore import Qt, QTimer
from modules.engine.Buffer import Buffer
from modules.engine.Color import Color
from main_engine import *
from modules.game.Timer import Timer

class NoScrollTextEdit(QTextEdit):
  def wheelEvent(self, event):
    event.ignore()

class EmulatedTerminal(QWidget):
  def __init__(self, game_name="TEST"):
    super().__init__()
    self.game_name = game_name
    self.font_size = 14
    self.font_color = "#00ff5e"
    self.capture_active = False
    self.captured_key = None
    
    self.color_cache = {}  # Cache pour les couleurs calculées
  
    self.buffer = None
    self.game_run = None
    self.player_run = None
    self.timer_game = None
    self.fight_game = None

    self.game_timer = QTimer(self) # Create a QTimer for the game loop
    self.game_timer.timeout.connect(self.update_game) # Connect its timeout signal to our update method

    self.setup_ui()
    self.init_game_logic()

  def setup_ui(self):
    self.setWindowTitle(self.game_name)
    self.setStyleSheet("background-color: black;")

    self.setWindowModality(Qt.WindowModality.ApplicationModal)

    # Désactive les boutons minimiser / maximiser
    self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)
    self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)

    # Layout principal
    self.terminal_layout = QVBoxLayout(self)
    self.terminal_layout.setSpacing(0)
    self.terminal_layout.setContentsMargins(0, 0, 0, 0)

    # QTextEdit configuré une fois pour toutes
    self.text_edit = NoScrollTextEdit()
    self.text_edit.setAcceptRichText(True)
    self.text_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.text_edit.setStyleSheet(f"font-size: {self.font_size}pt; font-family: Consolas, 'Courier New', monospace;")
    self.text_edit.setReadOnly(True)
    self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.FixedColumnWidth)
    self.text_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    self.text_edit.setUndoRedoEnabled(False)

    self.terminal_layout.addWidget(self.text_edit)

    # Affiche la fenêtre maximisée une fois tout configuré
    self.showMaximized()
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

  def getWidth(self):
    return self.terminal_width
  
  def getHeight(self):
    return self.terminal_height

  def get_cached_color(self, color, depth):
    """Cache les couleurs calculées pour éviter les recalculs"""
    cache_key = (color, depth)
    if cache_key not in self.color_cache:
      if depth:
        depth_factor = (1 - (max(2, min(6, depth)) / 8)) * 1.1
        color_lst = [
          int(Color.get_red(color) * depth_factor),
          int(Color.get_green(color) * depth_factor), 
          int(Color.get_blue(color) * depth_factor)
        ]
      else:
        color_lst = [
          Color.get_red(color),
          Color.get_green(color),
          Color.get_blue(color)
        ]
      self.color_cache[cache_key] = f"#{color_lst[0]:02x}{color_lst[1]:02x}{color_lst[2]:02x}"
    
    return self.color_cache[cache_key]

  def showBuffer(self):
    if self.buffer:
      html_parts = []
      
      for line in self.buffer.get_data():
        for charPack in line:
          character = charPack[0]
          char_color = self.get_cached_color(charPack[1], charPack[2])
          if character == ' ':
            character = "&nbsp;"
          html_parts.append(f'<span style="color:{char_color};">{character}</span>')
        html_parts.append("<br>")
      
      # Une seule opération de concaténation
      self.text_edit.setHtml(''.join(html_parts))
      self.update()

  def clearBuffer(self):
    Buffer.clear_data(self.buffer, self)
    self.showBuffer()

  def getKey(self):
    key_to_return = self.captured_key
    self.captured_key = None # Clear after reading
    return key_to_return

  def keyPressEvent(self, event: QKeyEvent):
    self.captured_key = event.key()

  def resizeEvent(self, event):
    super().resizeEvent(event)
    # À chaque redimensionnement, on recalcule le nombre de colonnes/ligues
    metrics = QFontMetrics(QFont("Consolas", self.font_size))
    fw = metrics.horizontalAdvance('W')
    fh = metrics.height()

    self.terminal_width = round(self.width() / fw) - 1
    self.terminal_height = round(self.height() / fh) - 1

    self.text_edit.setLineWrapColumnOrWidth(self.terminal_width)
    self.text_edit.setMinimumWidth(self.terminal_width * fw)

    self.buffer = Buffer(self)

  def init_game_logic(self):
    # Démarrage du gestionnaire de couleurs :
    wall_pink = Color(189, 0, 255)
    blue_cyber = Color(0,255,159)

    self.game_run = Game(0.01, "workingDir/data.json")
    self.game_run.set_color1(wall_pink)
    self.game_run.set_color2(blue_cyber)
    self.game_run.upload_all_end("workingDir/data.json")

    self.player_run = Player("workingDir/data.json", 80, -(math.pi/2))

    NPC.dispatch_NPCS(self.game_run, "workingDir/data.json")

    self.fight_game = Fight(self)
    Enemy.dispatch_Enemies(self.fight_game, "workingDir/data.json")

    self.game_run.set_fight(self.fight_game)

    self.timer_game = Timer("workingDir/data.json", Color(255,0,0))

    self.starting_game_time = time.time()
    
    self.game_timer.start(16) 

  def update_game(self):
    # This method is called periodically by the QTimer
    dt = self.game_run.get_diff_time()
    key = self.getKey() # Get the last captured key

    if key == Qt.Key.Key_Escape:  # Quitter avec 'échap'
      sys.exit()
    elif key == Qt.Key.Key_Z:
      position = self.player_run.get_position()
      n_pos = [position[0] + dt * 5 * math.cos(self.player_run.get_angle()), position[1] + dt * 5 * math.sin(self.player_run.get_angle())]
      self.player_run.set_position(n_pos[0], n_pos[1])
    elif key == Qt.Key.Key_S:
      position = self.player_run.get_position()
      n_pos = [position[0] - dt * 5 * math.cos(self.player_run.get_angle()), position[1] - dt * 5 * math.sin(self.player_run.get_angle())]
      self.player_run.set_position(n_pos[0], n_pos[1])
    elif key == Qt.Key.Key_Q:
      self.player_run.set_angle(self.player_run.get_angle() + dt*5)
    elif key == Qt.Key.Key_D:
      self.player_run.set_angle(self.player_run.get_angle() - dt*5)
    
    if self.fight_game.is_fight_time(self.player_run)[0] :
      if key == Qt.Key.Key_Space :
        (self.game_run.get_fight()).set_flame_state(1)
        Enemy.shoot_enemy(self.fight_game.is_fight_time(self.player_run)[1], self, self.game_run.get_fight())

    if self.game_run.get_map()[int(self.player_run.get_position()[1])][int(self.player_run.get_position()[0])] :
      endGame(self, self.game_run, 0)
      return
    
    self.clearBuffer()

    self.timer_game.show_timer(self)
    self.timer_game.remove_time(self.starting_game_time-time.time())
    drawFloor(self, self.game_run)
    get_rays(self, self.game_run, self.player_run)
    draw_NPC(self, self.game_run, self.player_run, Color(0,255,159))
    if self.fight_game.is_fight_time(self.player_run)[0] :
      Enemy.draw_Enemy(self, self.game_run.get_fight(), self.player_run, Color(0,255,159))
      self.fight_game.update_fight(self, Color(0,255,159)) 
    self.showBuffer()
    self.game_run.running_time()

    if self.timer_game.get_remaining_time() < 0 :
      endGame(self, self.game_run, 0)

  def closeEvent(self, event):
    self.game_timer.stop()
    event.accept()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  terminal = EmulatedTerminal()
  sys.exit(app.exec())
