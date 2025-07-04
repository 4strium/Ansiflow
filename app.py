import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QGridLayout, QCheckBox, QSizePolicy, QPushButton, QStackedLayout
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QAction
from PyQt6.QtCore import Qt
from modules.starting import StartWindow
from modules.grid import GridWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtGui import QPainter, QColor, QPen

class MainWindow(QMainWindow):

  def __init__(self):
    super().__init__()
    self.border_color = "#000000"
    self.checked_bg_color = "#262626"
    self.last_tab = None
    self.startup()

  def startup(self) :
    self.sw = StartWindow()
    self.sw.show()
    self.sw.finished.connect(self.handleStartupFinished)

  def handleStartupFinished(self):
    if self.sw.getStartup_finished() :
      self.sw.close()
      self.initializeUI()

  def initializeUI(self):
    self.setWindowTitle("Patate - The 3D ASCII Game Engine")
    self.setMinimumSize(1000,650)
    self.showMaximized()

    # Load the custom fonts
    font_id_calsans = QFontDatabase.addApplicationFont("fonts/CalSans.ttf")
    font_families_calsans = QFontDatabase.applicationFontFamilies(font_id_calsans)
    if font_families_calsans:
      self.calSans = font_families_calsans[0]
    else:
      self.calSans = "Arial"

    font_id_huninn = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families_huninn = QFontDatabase.applicationFontFamilies(font_id_huninn)
    if font_families_huninn:
      self.hunnin = font_families_huninn[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()
    self.createActions()
    self.createMenu()
    self.show()

  def setUpWindow(self):
    stylesheet_main_layout = """
      QWidget#Map, QWidget#Tools {
        border-radius : 25px;
        background-color : #ebebeb;
      }
    """
    self.title_map = QLabel("La Carte")
    self.title_map.setFont(QFont(self.calSans, 36))
    self.title_map.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    
    self.grid_map = QWidget()
    self.generateGrid()

    self.map_layout = QVBoxLayout()
    self.map_layout.addWidget(self.title_map)
    self.map_layout.addWidget(self.grid_map, stretch=1)

    self.title_tools = QLabel("Les Outils")
    self.title_tools.setFont(QFont(self.calSans, 36))
    self.title_tools.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    stylesheet_player = """
      QPushButton {
        background-color: white;
        border-top-left-radius: 25px;
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
        border-bottom-left-radius: 25px;
        padding: 15px;
        margin: 0px;
      }
      QPushButton:hover {
        background-color: #c9c9c9;
      }
    """
    self.player_button = QPushButton("Joueur")
    self.player_button.setFont(QFont(self.hunnin,22))
    self.player_button.setStyleSheet(stylesheet_player)
    self.player_button.pressed.connect(self.switchToolsTabs)

    stylesheet_middle = """
      QPushButton {
        background-color: white;
        padding: 15px;
        margin: 0px;
        border-radius: 0px;
      }
      QPushButton:hover {
        background-color: #c9c9c9;
      }
    """
    self.walls_button = QPushButton("Murs")
    self.walls_button.setFont(QFont(self.hunnin,22))
    self.walls_button.setStyleSheet(stylesheet_middle)
    self.walls_button.pressed.connect(self.switchToolsTabs)
    self.enemies_button = QPushButton("Ennemis")
    self.enemies_button.setFont(QFont(self.hunnin,22))
    self.enemies_button.setStyleSheet(stylesheet_middle)
    self.enemies_button.pressed.connect(self.switchToolsTabs)

    stylesheet_npc = """
      QPushButton {
        background-color : white;
        border-top-left-radius: 0px;
        border-top-right-radius: 25px;
        border-bottom-right-radius: 25px;
        border-bottom-left-radius: 0px;
        padding : 15px;
        margin: 0px;
      }
      QPushButton:hover {
        background-color: #c9c9c9;
      }
    """
    self.npc_button = QPushButton("Personnages")
    self.npc_button.setFont(QFont(self.hunnin,22))
    self.npc_button.setStyleSheet(stylesheet_npc)
    self.npc_button.pressed.connect(self.switchToolsTabs)

    self.tabs_selectors = QHBoxLayout()
    self.tabs_selectors.addWidget(self.player_button)
    self.tabs_selectors.addWidget(self.walls_button)
    self.tabs_selectors.addWidget(self.enemies_button)
    self.tabs_selectors.addWidget(self.npc_button)
    self.tabs_selectors.setContentsMargins(20, 0, 0, 20)
    self.tabs_selectors.setSpacing(0)
    self.tabs_selectors.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    # Page 1 :
    page1_infotext = QLabel("Sur la carte ci-contre, cliquez sur la case où votre joueur apparaîtra au lancement du jeu.")
    page1_infotext.setFont(QFont(self.hunnin, 22))
    page1_infotext.setAlignment(Qt.AlignmentFlag.AlignCenter)
    page1_infotext.setWordWrap(True)

    purple_square = QLabel()
    purple_square.setFixedSize(40, 40)
    purple_square.setStyleSheet("background-color: #a259f7; border-radius: 0px;")
    purple_square.setAlignment(Qt.AlignmentFlag.AlignCenter)

    page1_legendtext = QLabel("Case d'apparition")
    page1_legendtext.setFont(QFont(self.hunnin, 22))
    page1_legendtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

    page1_legend = QHBoxLayout()
    page1_legend.setSpacing(20)
    page1_legend.addStretch()
    page1_legend.addWidget(purple_square, alignment=Qt.AlignmentFlag.AlignCenter)
    page1_legend.addWidget(page1_legendtext, alignment=Qt.AlignmentFlag.AlignCenter)
    page1_legend.addStretch()

    page1_layout = QVBoxLayout()
    page1_layout.addWidget(page1_infotext)
    page1_layout.addLayout(page1_legend)
    page1_container = QWidget()
    page1_container.setLayout(page1_layout)

    # Page 2 :
    btn_tools_stylesheet = """
        QPushButton {
          background-color: white;
          padding: 15px;
          margin: 0px;
          border-radius: 25px;
        }
        QPushButton:hover {
          background-color: #c9c9c9;
        }
    """
    page2_infotext = QLabel("Sélectionnez l'outil :")
    page2_infotext.setFont(QFont(self.hunnin, 22))
    page2_infotext.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Créer un QPixmap pour l'icône + vert
    plus_pixmap = QPixmap(24, 24)
    plus_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(plus_pixmap)
    pen = QPen(QColor("#00ff5e"), 4)
    painter.setPen(pen)
    painter.drawLine(12, 4, 12, 20)
    painter.drawLine(4, 12, 20, 12)
    painter.end()
    plus_icon = QIcon(plus_pixmap)
    page2_addbutton = QPushButton(" Ajouter des murs")
    page2_addbutton.setIcon(plus_icon)
    page2_addbutton.setIconSize(plus_pixmap.size())
    page2_addbutton.setFont(QFont(self.hunnin, 22))
    page2_addbutton.setStyleSheet(btn_tools_stylesheet)

    # Créer un QPixmap pour l'icône - rouge
    subs_pixmap = QPixmap(24, 24)
    subs_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(subs_pixmap)
    pen = QPen(QColor("#f81111"), 4)
    painter.setPen(pen)
    painter.drawLine(4, 12, 20, 12)
    painter.end()
    subs_icon = QIcon(subs_pixmap)
    page2_subsbutton = QPushButton(" Supprimer des murs")
    page2_subsbutton.setIcon(subs_icon)
    page2_subsbutton.setIconSize(subs_pixmap.size())
    page2_subsbutton.setFont(QFont(self.hunnin, 22))
    page2_subsbutton.setStyleSheet(btn_tools_stylesheet)
    page2_legendtext = QLabel("""Tous les murs extérieurs sont immuables.\nLa fin du jeu s'effectue donc obligatoirement par la discussion avec un personnage spécifié.""")
    page2_legendtext.setWordWrap(True)
    page2_legendtext.setFont(QFont(self.hunnin, 18))
    page2_legendtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

    page2_layout = QVBoxLayout()
    page2_layout.addWidget(page2_infotext, stretch=1)
    page2_layout.addWidget(page2_addbutton, stretch=1)
    page2_layout.setSpacing(10)
    page2_layout.addWidget(page2_subsbutton, stretch=1)
    page2_layout.addWidget(page2_legendtext, stretch=2)
    page2_container = QWidget()
    page2_container.setLayout(page2_layout)

    # Page 3 :
    page3_infotext = QLabel("Sur la carte ci-contre, cliquez sur les cases où vous désirez positionner des ennemis.")
    page3_infotext.setFont(QFont(self.hunnin, 22))
    page3_infotext.setWordWrap(True)
    page3_infotext.setAlignment(Qt.AlignmentFlag.AlignCenter)
    green_square = QLabel()
    green_square.setFixedSize(40, 40)
    green_square.setStyleSheet("background-color: #00ff5e; border-radius: 0px;")
    page3_legendtext = QLabel("Ennemis")
    page3_legendtext.setFont(QFont(self.hunnin, 22))

    page3_legend = QHBoxLayout()
    page3_legend.setSpacing(20)
    page3_legend.addStretch()
    page3_legend.addWidget(green_square, alignment=Qt.AlignmentFlag.AlignLeft)
    page3_legend.addWidget(page3_legendtext, alignment=Qt.AlignmentFlag.AlignLeft)
    page3_legend.addStretch()

    page3_layout = QVBoxLayout()
    page3_layout.addWidget(page3_infotext)
    page3_layout.addLayout(page3_legend)
    page3_container = QWidget()
    page3_container.setLayout(page3_layout)

    # Page 4 :
    page4_container = QWidget()

    self.stacked_tools = QStackedLayout()
    self.stacked_tools.addWidget(page1_container)
    self.stacked_tools.addWidget(page2_container)
    self.stacked_tools.addWidget(page3_container)
    self.stacked_tools.addWidget(page4_container)
    self.stacked_tools.setCurrentIndex(2)

    self.tools_layout = QVBoxLayout()
    self.tools_layout.addWidget(self.title_tools, stretch=1)
    self.tools_layout.addLayout(self.tabs_selectors, stretch=1)
    self.tools_layout.addLayout(self.stacked_tools, stretch=8)

    self.map_widget = QWidget()
    self.map_widget.setObjectName("Map")
    self.map_widget.setLayout(self.map_layout)
    self.tools_widget = QWidget()
    self.tools_widget.setObjectName("Tools")
    self.tools_widget.setLayout(self.tools_layout)

    self.main_layout = QHBoxLayout()
    self.main_layout.setContentsMargins(20, 0, 20, 20)
    self.main_layout.addWidget(self.map_widget, stretch=2)
    self.main_layout.addSpacing(int(self.width() * 0.01))
    self.main_layout.addWidget(self.tools_widget, stretch=1)
    self.setStyleSheet(stylesheet_main_layout)

    self.central_widget = QWidget()
    self.central_widget.setLayout(self.main_layout)
    self.setCentralWidget(self.central_widget)

    self.player_button.click()

  def generateGrid(self):
    self.map_size = self.sw.getMap_size()
    
    if self.map_size == -1:
      return

    # on remplace self.grid_map (un QWidget vide) par notre GridWidget
    self.grid_map = GridWidget(map_size=self.map_size, border_color=self.border_color, checked_bg_color=self.checked_bg_color)

  def switchToolsTabs(self):
    sender = self.sender()
    if sender :
      # Reset last button before :
      if self.last_tab :
        self.last_tab[0].setStyleSheet(self.last_tab[1])
        self.last_tab[0].setFont(QFont(self.hunnin, 22))
      currentStyle = sender.styleSheet()
      self.last_tab = [sender, currentStyle]
      newStyle = """
        QPushButton {
            color : white;
            background-color: #29e2ff;
          }
        QPushButton:hover {
            background-color: #29e2ff;
          }
      """
      sender.setStyleSheet(currentStyle+newStyle)
      sender.setFont(QFont(self.calSans, 30))
    # Set the current tab in the stacked layout based on which button was pressed
    if sender == self.player_button:
      self.stacked_tools.setCurrentIndex(0)
    elif sender == self.walls_button:
      self.stacked_tools.setCurrentIndex(1)
    elif sender == self.enemies_button:
      self.stacked_tools.setCurrentIndex(2)
    elif sender == self.npc_button:
      self.stacked_tools.setCurrentIndex(3)

  def createActions(self):
    self.quit_act = QAction("&Quitter")
    self.quit_act.setShortcut("Ctrl+Q")
    self.quit_act.triggered.connect(self.close)

  def createMenu(self):
    file_menu = self.menuBar().addMenu("Fichier")
    file_menu.addAction(self.quit_act)

    edit_menu = self.menuBar().addMenu("Edition")
    exec_menu = self.menuBar().addMenu("Exécution")
    help_menu = self.menuBar().addMenu("Aide")

  def maintainSpacingLayout(self):
    self.main_layout.setSpacing(int(self.width() * 0.01))

  def resizeTitles(self):
    responsive_font_size = min(self.width()//24, self.height()//24)
    self.title_map.setFont(QFont(self.calSans, responsive_font_size))
    self.title_tools.setFont(QFont(self.calSans, responsive_font_size))

  def resizeEvent(self, event):
    if hasattr(self, 'main_layout'):
      self.maintainSpacingLayout()
    if hasattr(self, 'title_map'):
      self.resizeTitles()
    super().resizeEvent(event)
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec())