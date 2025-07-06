import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QTextEdit
from PyQt6.QtGui import QFont, QFontMetrics, QKeyEvent
from PyQt6.QtCore import Qt, QTimer
from modules.engine.Buffer import Buffer
from modules.engine.Color import Color
from main_engine import *

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
    
    self.buffer = None
    self.setup_ui()

  def setup_ui(self):
    self.setWindowTitle(self.game_name)
    self.setStyleSheet("background-color: black;")

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

    self.terminal_layout.addWidget(self.text_edit)

    # Affiche la fenêtre maximisée une fois tout configuré
    self.showMaximized()
    QTimer.singleShot(0, self.run)

  def getWidth(self):
    return self.terminal_width
  
  def getHeight(self):
    return self.terminal_height

  def showBuffer(self):
    if self.buffer :
      
      html_content = ""

      for line in self.buffer.get_data():
        for charPack in line :
          character = charPack[0]
          if charPack[2] :
            depth_factor = (1 - (max(2, min(6, charPack[2])) / 8))*1.1
            color_lst = [int(Color.get_red(charPack[1]) * depth_factor),int(Color.get_green(charPack[1]) * depth_factor), int(Color.get_blue(charPack[1]) * depth_factor)]
          else :
            color_lst = [Color.get_red(charPack[1]),Color.get_green(charPack[1]),Color.get_blue(charPack[1])]
          char_color = f"rgb({color_lst[0]} {color_lst[1]} {color_lst[2]})" 
          html_content += f"""<span style="color : {char_color};">{character}</span>"""
        html_content += "</br>"

      self.text_edit.setHtml(html_content)

  def clearBuffer(self):
    Buffer.clear_data(self.buffer)
    self.showBuffer()

  def getKey(self):
    self.capture_active = True
    self.captured_key = None
    self.setFocus()
    time.sleep(0.1)
    return self.captured_key

  def keyPressEvent(self, event: QKeyEvent):
    if self.capture_active:
      key = event.key()
      self.capture_active = False
      self.captured_key = key

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

  def interact(self, game_inp,player,window):
    dt = Game.get_diff_time(game_inp)
    key = self.getKey()

    if key == 27:  # Quitter avec 'échap'
      sys.exit()
      exit()
    elif key == ord('z'):
      # Simuler l'avancement du personnage :
      position = Player.get_position(player)
      n_pos = [position[0] + dt * 5 * math.cos(Player.get_angle(player)),position[1]+ dt * 5 * math.sin(Player.get_angle(player))]
      Player.set_position(player,n_pos[0],n_pos[1])
      Buffer.clear_data(window)
    elif key == ord('s'):
      # Simuler le reculement du personnage par rapport au sol :
      position = Player.get_position(player)
      n_pos = [position[0] - dt * 5 * math.cos(Player.get_angle(player)),position[1] - dt * 5 * math.sin(Player.get_angle(player))]
      Player.set_position(player,n_pos[0],n_pos[1])
      Buffer.clear_data(window) 
    elif key == ord('q'):
      Player.set_angle(player, player.get_angle() + dt*5)
      Buffer.clear_data(window)
    elif key == ord('d'):
      Player.set_angle(player, player.get_angle() - dt*5)
      Buffer.clear_data(window)

    if Fight.is_fight_time(Game.get_fight(game_inp),player)[0] :
      if key == 32 :
        (Game.get_fight(game_inp)).set_flame_state(1)
        Enemy.shoot_enemy(Fight.is_fight_time(Game.get_fight(game_inp),player)[1],window,Game.get_fight(game_inp))

  def run(self):
    self.showMaximized()

    # Démarrage du gestionnaire de couleurs :
    wall_pink = Color(189, 0, 255)
    blue_cyber = Color(0,255,159)

    game_run = Game(0.01, "workingDir/data.json")
    Game.set_color1(game_run, wall_pink)
    Game.set_color2(game_run, blue_cyber)
    Game.upload_all_end(game_run,"workingDir/data.json")

    player_run = Player("workingDir/data.json",80,-(math.pi/2))

    NPC.dispatch_NPCS(game_run,"workingDir/data.json")

    fight_game = Fight(self)
    Enemy.dispatch_Enemies(fight_game,"workingDir/data.json")

    Game.set_fight(game_run,fight_game)

    timer_game = Timer("workingDir/data.json", Color(255,0,0))

    starting_game_time = time.time()

    # Boucle de simulation :
    while True :
      self.interact(game_run,player_run,self.buffer)

      if Game.get_map(game_run)[int(Player.get_position(player_run)[1])][int(Player.get_position(player_run)[0])] :
        print("CHECKPOINT1")
        endGame(self, self.buffer,game_run, 0)
        break
      print((self.getWidth(), self.getHeight()))

      Timer.show_timer(timer_game,self)
      Timer.remove_time(timer_game,starting_game_time-time.time())
      drawFloor(self, game_run)
      get_rays(self, game_run, player_run)
      draw_NPC(self.buffer,game_run,player_run,blue_cyber)
      if Fight.is_fight_time(Game.get_fight(game_run),player_run)[0] :
        Enemy.draw_Enemy(self.buffer,Game.get_fight(game_run),player_run,blue_cyber)
        Fight.update_fight(Game.get_fight(game_run),self,blue_cyber)
      self.showBuffer()
      Game.running_time(game_run)
      time.sleep(Game.get_diff_time(game_run)) # Faire varier le rafraichissment des animations

      if Timer.get_remaining_time(timer_game) < 0 :
        endGame(self, self.buffer, game_run,0)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  terminal = EmulatedTerminal()
  sys.exit(app.exec())
