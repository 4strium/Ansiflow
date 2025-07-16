import sys, os, time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QComboBox, QPushButton, QStackedLayout, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QAction
from PyQt6.QtCore import Qt
from modules.starting import StartWindow
from modules.grid import GridWidget
from modules.newNPC import NewNPC
from modules.removeNPC import RemoveNPC
from modules.game import NPC
from modules.bloc import Bloc
from emulatedTerminal import EmulatedTerminal
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QCursor
from scripts.image_to_ascii import image_to_ascii_by_color

class MainWindow(QMainWindow):

  def __init__(self):
    super().__init__()

    self.border_color = "#000000"
    self.checked_bg_color = "#262626"
    self.player_color = "#a259f7"
    self.enemy_color = "#00ff5e"
    self.enemy_path = None
    self.last_tab = None
    self.last_mode = None
    self.nb_perso = 0
    self.pers_limit = 0
    self.pers_colors = []
    self.current_NPC_selected = None
    self.NPCs = []
    self.saved_NPCs = {}
    self.bloc_zone = []
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
    self.setMinimumSize(1250,650)
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

    title_working_zone = QLabel("Le Schéma du Dialogue")
    title_working_zone.setFont(QFont(self.calSans, 36))
    title_working_zone.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    self.bloc_working_zone = QWidget()
    self.bloc_layout = QVBoxLayout()
    self.bloc_layout.addWidget(title_working_zone)
    self.bloc_layout.addWidget(self.bloc_working_zone, stretch=1)

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
    self.player_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
    self.walls_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.walls_button.pressed.connect(self.switchToolsTabs)
    self.enemies_button = QPushButton("Ennemis")
    self.enemies_button.setFont(QFont(self.hunnin,22))
    self.enemies_button.setStyleSheet(stylesheet_middle)
    self.enemies_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
    self.npc_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
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
    purple_square.setStyleSheet(f"""background-color: {self.player_color}; border-radius: 0px;""")
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
    self.page2_addbutton = QPushButton(" Ajouter des murs")
    self.page2_addbutton.setIcon(plus_icon)
    self.page2_addbutton.setIconSize(plus_pixmap.size())
    self.page2_addbutton.setFont(QFont(self.hunnin, 22))
    self.page2_addbutton.setStyleSheet(btn_tools_stylesheet)
    self.page2_addbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.page2_addbutton.pressed.connect(self.activateWallTool)

    # Créer un QPixmap pour l'icône - rouge
    subs_pixmap = QPixmap(24, 24)
    subs_pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(subs_pixmap)
    pen = QPen(QColor("#f81111"), 4)
    painter.setPen(pen)
    painter.drawLine(4, 12, 20, 12)
    painter.end()
    subs_icon = QIcon(subs_pixmap)
    self.page2_subsbutton = QPushButton(" Supprimer des murs")
    self.page2_subsbutton.setIcon(subs_icon)
    self.page2_subsbutton.setIconSize(subs_pixmap.size())
    self.page2_subsbutton.setFont(QFont(self.hunnin, 22))
    self.page2_subsbutton.setStyleSheet(btn_tools_stylesheet)
    self.page2_subsbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.page2_subsbutton.pressed.connect(self.activateWallTool)

    page2_legendtext = QLabel("""Tous les murs extérieurs sont immuables.\nLa fin du jeu s'effectue donc obligatoirement par la discussion avec un personnage spécifié.""")
    page2_legendtext.setWordWrap(True)
    page2_legendtext.setFont(QFont(self.hunnin, 18))
    page2_legendtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

    page2_layout = QVBoxLayout()
    page2_layout.addWidget(page2_infotext, stretch=1)
    page2_layout.addWidget(self.page2_addbutton, stretch=1)
    page2_layout.setSpacing(10)
    page2_layout.addWidget(self.page2_subsbutton, stretch=1)
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
    page3_legend.addStretch()
    page3_legend.addWidget(green_square, alignment=Qt.AlignmentFlag.AlignLeft)
    page3_legend.addWidget(page3_legendtext, alignment=Qt.AlignmentFlag.AlignLeft)
    page3_legend.addStretch()
    page3_legend.setAlignment(Qt.AlignmentFlag.AlignTop)

    page3_skin = QPushButton("Sélectionner l'apparence des ennemis")
    page3_skin.setFont(QFont(self.hunnin, 22))
    page3_skin.setStyleSheet(btn_tools_stylesheet)
    page3_skin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    page3_skin.pressed.connect(self.changeEnemySkin)

    self.page3_infoskin = QLabel("Attention : L'apparence n'est pas définie !")
    self.page3_infoskin.setFont(QFont(self.hunnin, 18))
    self.page3_infoskin.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.page3_infoskin.setWordWrap(True)
    self.page3_infoskin.setStyleSheet("color : #f81111;")

    page3_layout = QVBoxLayout()
    page3_layout.addWidget(page3_infotext, stretch=1)
    page3_layout.addLayout(page3_legend, stretch=1)
    page3_layout.addWidget(page3_skin, stretch=1)
    page3_layout.addWidget(self.page3_infoskin, stretch=1)

    page3_container = QWidget()
    page3_container.setLayout(page3_layout)

    # Page 4 :
    page4_title = QLabel("Vos personnages :")
    page4_title.setFont(QFont(self.hunnin, 22))
    page4_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.page4_table = QTableWidget()
    self.page4_table.setColumnCount(3)
    self.page4_table.setHorizontalHeaderLabels(["Nom", "Couleur", "Attributs"])
    self.page4_table.setRowCount(self.nb_perso)
    
    self.page4_table.setFont(QFont(self.hunnin, 15))
    self.page4_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.page4_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.page4_table.setAlternatingRowColors(True)
    self.page4_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    self.page4_table.verticalHeader().setVisible(False)
    self.page4_table.verticalHeader().setDefaultSectionSize(50)
  
    self.page4_addbutton = QPushButton(" Ajouter un personnage")
    self.page4_addbutton.setIcon(plus_icon)
    self.page4_addbutton.setIconSize(plus_pixmap.size())
    self.page4_addbutton.setFont(QFont(self.hunnin, 22))
    self.page4_addbutton.setStyleSheet(btn_tools_stylesheet)
    self.page4_addbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.page4_addbutton.pressed.connect(self.createNewPerso)

    self.page4_subsbutton = QPushButton(" Supprimer un personnage")
    self.page4_subsbutton.setIcon(subs_icon)
    self.page4_subsbutton.setIconSize(subs_pixmap.size())
    self.page4_subsbutton.setFont(QFont(self.hunnin, 22))
    self.page4_subsbutton.setStyleSheet(btn_tools_stylesheet)
    self.page4_subsbutton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.page4_subsbutton.pressed.connect(self.deletePersoDialog)
    
    self.page4_limit_text = QLabel(f"(limité à {self.pers_limit} personnages)")
    self.page4_limit_text.setFont(QFont(self.hunnin, 14))
    self.page4_limit_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    page4_layout = QVBoxLayout()
    page4_layout.addWidget(page4_title, stretch=1)
    page4_layout.addWidget(self.page4_table, stretch=4)
    page4_layout.addWidget(self.page4_addbutton, stretch=2)
    page4_layout.addWidget(self.page4_subsbutton, stretch=2)
    page4_layout.addWidget(self.page4_limit_text, stretch=1)

    page4_container = QWidget()
    page4_container.setLayout(page4_layout)

    self.stacked_tools = QStackedLayout()
    self.stacked_tools.addWidget(page1_container)
    self.stacked_tools.addWidget(page2_container)
    self.stacked_tools.addWidget(page3_container)
    self.stacked_tools.addWidget(page4_container)

    self.tools_layout = QVBoxLayout()
    self.tools_layout.addWidget(self.title_tools, stretch=1)
    self.tools_layout.addLayout(self.tabs_selectors, stretch=1)
    self.tools_layout.addLayout(self.stacked_tools, stretch=8)

    # Page 2 - Right Side :
    config_question = QLabel("Que souhaitez-vous configurer ?")
    config_question.setFont(QFont(self.hunnin, 22))
    config_question.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.answer_pos = QPushButton("Emplacement du personnage sur la carte")
    self.answer_pos.setFont(QFont(self.hunnin, 22))
    self.answer_pos.setStyleSheet(btn_tools_stylesheet)
    self.answer_pos.setCursor(Qt.CursorShape.PointingHandCursor)
    self.answer_pos.pressed.connect(self.selectNPCposition)

    self.answer_dial = QPushButton("Dialogues")
    self.answer_dial.setFont(QFont(self.hunnin, 22))
    self.answer_dial.setStyleSheet(btn_tools_stylesheet)
    self.answer_dial.setCursor(Qt.CursorShape.PointingHandCursor)
    self.answer_dial.pressed.connect(self.defineConversation)

    self.answer_skin = QPushButton("Apparences")
    self.answer_skin.setFont(QFont(self.hunnin, 22))
    self.answer_skin.setStyleSheet(btn_tools_stylesheet)
    self.answer_skin.setCursor(Qt.CursorShape.PointingHandCursor)
    self.answer_skin.pressed.connect(self.defineSkins)

    close_css = """
      QPushButton:hover {
        background-color: #c9c9c9;
      }
    """
    self.close_button = QPushButton("Fermer")
    self.close_button.setFont(QFont(self.calSans, 18))
    self.close_button.pressed.connect(self.switchRightSide)
    self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
    self.close_button.setStyleSheet(close_css)

    blank_space = QWidget()
    spacing_layout = QHBoxLayout()
    spacing_layout.addWidget(blank_space, stretch=3)
    spacing_layout.addWidget(self.close_button, stretch=1)

    # Crée un layout pour les boutons de configuration
    buttons_layout = QVBoxLayout()
    buttons_layout.addWidget(self.answer_pos)
    buttons_layout.addWidget(self.answer_dial)
    buttons_layout.addWidget(self.answer_skin)

    # Ajoute des stretches pour centrer verticalement
    config_layout = QVBoxLayout()
    config_layout.addStretch(1)
    config_layout.addWidget(config_question, alignment=Qt.AlignmentFlag.AlignCenter)
    config_layout.addSpacing(20)
    config_layout.addLayout(buttons_layout)
    config_layout.addStretch(1)
    config_layout.addLayout(spacing_layout)

    # Page 3 - Right Side :
    pers_pos_infotext1 = QLabel("Veuillez cliquer sur la case où vous souhaitez positionner votre personnage.")
    pers_pos_infotext1.setFont(QFont(self.hunnin, 22))
    pers_pos_infotext1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pers_pos_infotext1.setWordWrap(True)
    pers_pos_infotext2 = QLabel("Attention, il ne doit pas être trop proche d'un ennemi ou d'un autre personnage.")
    pers_pos_infotext2.setFont(QFont(self.hunnin, 22))
    pers_pos_infotext2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pers_pos_infotext2.setWordWrap(True)

    pers_pos_layout = QVBoxLayout()
    pers_pos_close_button = QPushButton("Fermer")
    pers_pos_close_button.setFont(QFont(self.calSans, 18))
    pers_pos_close_button.pressed.connect(self.switchRightSide)
    pers_pos_close_button.setCursor(Qt.CursorShape.PointingHandCursor)
    pers_pos_close_button.setStyleSheet(close_css)

    blank_space2 = QWidget()
    spacing_layout2 = QHBoxLayout()
    spacing_layout2.addWidget(blank_space2, stretch=3)
    spacing_layout2.addWidget(pers_pos_close_button, stretch=1)

    pers_pos_layout.addWidget(pers_pos_infotext1)
    pers_pos_layout.addWidget(pers_pos_infotext2)
    pers_pos_layout.addLayout(spacing_layout2)

    pers_pos_container = QWidget()
    pers_pos_container.setLayout(pers_pos_layout)

    # Page 4 - Right Side :
    self.pers_dialogue_layout = QVBoxLayout()
    bloc_btn_stylesheet = """
      QPushButton {
        background-color : white;
        color : black;
        border-radius : 10px;
        padding : 10px;
        padding-top: 4px;
        padding-bottom : 4px;
      }
      QPushButton:hover{
        background-color: #c9c9c9;
      }
    """

    bloc_combobox_stylesheet = """
      QComboBox {
        background-color : white;
        color : black;
        border-radius : 10px;
        padding : 10px;
        padding-top: 4px;
        padding-bottom : 4px;
      }
      QComboBox QAbstractItemView {
        background-color: white;
        color: black;
        selection-background-color: #c9c9c9;
        selection-color: black;
        padding: 4px;
      }
    """
    start_text = QLabel("DÉBUT")
    start_text.setFont(QFont(self.hunnin, 20))
    start_layout = QHBoxLayout()
    start_layout.setContentsMargins(0,0,0,0)
    start_layout.addWidget(start_text)
    start_container = QWidget()
    start_container.setLayout(start_layout)
    self.start_bloc = Bloc(self,0,1, start_container, "#00cf23", "#FFFFFF", 0, True)
    self.pers_dialogue_layout.addWidget(self.start_bloc)

    print_text_layout = QHBoxLayout()
    print_text_layout.setContentsMargins(0,0,0,0)
    afficher = QLabel("Afficher")
    afficher.setFont(QFont(self.hunnin, 20))
    texte_btn = QPushButton("texte")
    texte_btn.setFont(QFont(self.hunnin, 20))
    texte_btn.setStyleSheet(bloc_btn_stylesheet)
    texte_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    print_text_layout.addWidget(afficher)
    print_text_layout.addWidget(texte_btn)
    print_text = QWidget()
    print_text.setLayout(print_text_layout)
    self.pers_dialogue_layout.addWidget(Bloc(self,1,1, print_text, "#00ccff", "#FFFFFF", 1))

    ask_layout = QHBoxLayout()
    ask_layout.setContentsMargins(0,0,0,0)
    poser = QLabel("Poser")
    poser.setFont(QFont(self.hunnin, 20))
    ask_btn = QPushButton("question")
    ask_btn.setFont(QFont(self.hunnin, 20))
    ask_btn.setStyleSheet(bloc_btn_stylesheet)
    ask_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    a_text = QLabel("à")
    a_text.setFont(QFont(self.hunnin, 20))
    nb_answers_selector = QComboBox()
    nb_answers_selector.setFont(QFont(self.hunnin, 20))
    nb_answers_selector.setStyleSheet(bloc_combobox_stylesheet)
    nb_answers_selector.addItems(["2","3"])
    nb_answers_selector.setCursor(Qt.CursorShape.PointingHandCursor)
    answers_text = QLabel("réponses")
    answers_text.setFont(QFont(self.hunnin, 20))
    ask_layout.addWidget(poser)
    ask_layout.addWidget(ask_btn)
    ask_layout.addWidget(a_text)
    ask_layout.addWidget(nb_answers_selector)
    ask_layout.addWidget(answers_text)
    ask_container = QWidget()
    ask_container.setLayout(ask_layout)
    self.pers_dialogue_layout.addWidget(Bloc(self,1,3,ask_container, "#ff00b3", "#FFFFFF", 2))
    

    flux_text = QLabel("Regroupement des flux")
    flux_text.setFont(QFont(self.hunnin, 20))
    flux_layout = QHBoxLayout()
    flux_layout.setContentsMargins(0,0,0,0)
    flux_layout.addWidget(flux_text)
    flux_container = QWidget()
    flux_container.setLayout(flux_layout)
    self.pers_dialogue_layout.addWidget(Bloc(self,3,1,flux_container, "#7700e6", "#FFFFFF", 3))

    python_layout = QHBoxLayout()
    python_layout.setContentsMargins(0,0,0,0)
    executer = QLabel("Exécuter")
    executer.setFont(QFont(self.hunnin, 20))
    python_btn = QPushButton("code Python")
    python_btn.setFont(QFont(self.hunnin, 20))
    python_btn.setStyleSheet(bloc_btn_stylesheet)
    python_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    python_layout.addWidget(executer)
    python_layout.addWidget(python_btn)
    python_bloc_container = QWidget()
    python_bloc_container.setLayout(python_layout)
    self.pers_dialogue_layout.addWidget(Bloc(self,1,1, python_bloc_container, "#ff0000", "#FFFFFF", 4))

    end_text = QLabel("FIN")
    end_text.setFont(QFont(self.hunnin, 20))
    end_layout = QHBoxLayout()
    end_layout.setContentsMargins(0,0,0,0)
    end_layout.addWidget(end_text)
    end_container = QWidget()
    end_container.setLayout(end_layout)
    self.pers_dialogue_layout.addWidget(Bloc(self,1,0,end_container, "#ffae00", "#FFFFFF", 5, True))

    blank_space5 = QWidget()
    dialogue_close_button = QPushButton("Fermer")
    dialogue_close_button.setFont(QFont(self.calSans, 18))
    dialogue_close_button.pressed.connect(self.switchRightSide)
    dialogue_close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    dialogue_close_button.setStyleSheet(close_css)
    dialogue_close_button.setObjectName("saveDialog")

    dialogue_close_layout = QHBoxLayout()
    dialogue_close_layout.addWidget(blank_space5, stretch=3)
    dialogue_close_layout.addWidget(dialogue_close_button, stretch=1)

    self.pers_dialogue_layout.addLayout(dialogue_close_layout)

    perso_dialogue_container = QWidget()
    perso_dialogue_container.setLayout(self.pers_dialogue_layout)

    # Page 5 - Right Side :
    perso_skin_text = QLabel("Ajouter des apparences à votre personnage :")
    perso_skin_text.setFont(QFont(self.hunnin, 22))
    perso_skin_text.setWordWrap(True)
    perso_skin_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    perso_skin_1 = QPushButton("Apparence 1 (obligatoire)")
    perso_skin_1.setFont(QFont(self.hunnin, 22))
    perso_skin_1.setStyleSheet(btn_tools_stylesheet)
    perso_skin_1.setCursor(Qt.CursorShape.PointingHandCursor)
    perso_skin_1.pressed.connect(self.skinGetter)

    perso_skin_2 = QPushButton("Apparence 2 (facultative)")
    perso_skin_2.setFont(QFont(self.hunnin, 22))
    perso_skin_2.setStyleSheet(btn_tools_stylesheet)
    perso_skin_2.setCursor(Qt.CursorShape.PointingHandCursor)
    perso_skin_2.pressed.connect(self.skinGetter)

    perso_skin_3 = QPushButton("Apparence 3 (facultative)")
    perso_skin_3.setFont(QFont(self.hunnin, 22))
    perso_skin_3.setStyleSheet(btn_tools_stylesheet)
    perso_skin_3.setCursor(Qt.CursorShape.PointingHandCursor)
    perso_skin_3.pressed.connect(self.skinGetter)

    skins_group = QVBoxLayout()
    skins_group.addWidget(perso_skin_1)
    skins_group.addWidget(perso_skin_2)
    skins_group.addWidget(perso_skin_3)

    skin_close_button = QPushButton("Fermer")
    skin_close_button.setFont(QFont(self.calSans, 18))
    skin_close_button.pressed.connect(self.switchRightSide)
    skin_close_button.setCursor(Qt.CursorShape.PointingHandCursor)
    skin_close_button.setStyleSheet(close_css)
    blank_space4 = QWidget()
    spacing_layout4 = QHBoxLayout()
    spacing_layout4.addWidget(blank_space4, stretch=3)
    spacing_layout4.addWidget(skin_close_button, stretch=1)

    skin_layout = QVBoxLayout()
    skin_layout.addStretch(1)
    skin_layout.addWidget(perso_skin_text)
    skin_layout.addSpacing(20)
    skin_layout.addLayout(skins_group)
    skin_layout.addStretch(1)
    skin_layout.addLayout(spacing_layout4)

    skin_container = QWidget()
    skin_container.setLayout(skin_layout)

    self.right_layout = QStackedLayout()
    self.tools_container = QWidget()
    self.tools_container.setLayout(self.tools_layout)
    self.right_layout.addWidget(self.tools_container)
    self.config_container = QWidget()
    self.config_container.setLayout(config_layout)
    self.right_layout.addWidget(self.config_container)
    self.right_layout.addWidget(pers_pos_container)
    self.right_layout.addWidget(perso_dialogue_container)
    self.right_layout.addWidget(skin_container)
    self.right_layout.setCurrentIndex(0)

    self.left_layout = QStackedLayout()
    self.map_container = QWidget()
    self.map_container.setLayout(self.map_layout)
    self.bloc_container = QWidget()
    self.bloc_container.setLayout(self.bloc_layout)
    self.left_layout.addWidget(self.map_container)
    self.left_layout.addWidget(self.bloc_container)
    self.left_layout.setCurrentIndex(0)

    self.map_bloc_widget = QWidget()
    self.map_bloc_widget.setObjectName("Map")
    self.map_bloc_widget.setLayout(self.left_layout)
    self.tools_widget = QWidget()
    self.tools_widget.setObjectName("Tools")
    self.tools_widget.setLayout(self.right_layout)

    self.main_layout = QHBoxLayout()
    self.main_layout.setContentsMargins(20, 0, 20, 20)
    self.main_layout.addWidget(self.map_bloc_widget, stretch=2)
    self.main_layout.addSpacing(int(self.width() * 0.01))
    self.main_layout.addWidget(self.tools_widget, stretch=1)
    self.setStyleSheet(stylesheet_main_layout)

    self.central_widget = QWidget()
    self.central_widget.setLayout(self.main_layout)
    self.setCentralWidget(self.central_widget)

    self.player_button.click()

  def generateGrid(self):
    self.map_size = self.sw.getMap_size()
    self.pers_limit = self.map_size // 4
    
    if self.map_size == -1:
      return

    # on remplace self.grid_map (un QWidget vide) par notre GridWidget
    self.grid_map = GridWidget(self, self.map_size, self.border_color, self.checked_bg_color, self.player_color, self.enemy_color, self.enemy_path)
    self.grid_map.initJsonGrid() 

  def switchRightSide(self, mode = None):
    sender = self.sender()
    if sender :
      if sender.text() == "Configurer" :
        self.current_NPC_selected = sender.objectName()
        self.right_layout.setCurrentIndex(1)
      elif mode == 1 :
        self.right_layout.setCurrentIndex(2)
      elif mode == 2:
        self.right_layout.setCurrentIndex(3)
        self.left_layout.setCurrentIndex(1)
        self.resizeReleaseZone()
        self.openDialogWorkspace()
        QApplication.processEvents()
      elif mode == 3:
        self.right_layout.setCurrentIndex(4)
      elif sender.objectName() == "saveDialog" :
        self.saveDialogWorkspace()
        QApplication.processEvents()
        self.right_layout.setCurrentIndex(1)
        self.left_layout.setCurrentIndex(0)
      else :
        self.current_NPC_selected = None
        self.right_layout.setCurrentIndex(0)

  def switchToolsTabs(self):
    sender = self.sender()
    if sender :
      # Reset possible mode activation :
      if self.last_mode :        
        self.last_mode[0].setStyleSheet(self.last_mode[1])
        self.last_mode[0].setFont(QFont(self.hunnin, 22))
        self.last_mode = None
        self.grid_map.setMap_mode(0)
        self.grid_map.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
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
      self.grid_map.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      self.grid_map.setMap_mode(3)
    elif sender == self.walls_button:
      self.stacked_tools.setCurrentIndex(1)
      self.grid_map.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
      self.grid_map.setMap_mode(0)
    elif sender == self.enemies_button:
      self.stacked_tools.setCurrentIndex(2)
      self.grid_map.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      self.grid_map.setMap_mode(4)
    elif sender == self.npc_button:
      self.stacked_tools.setCurrentIndex(3)
      self.grid_map.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
      self.grid_map.setMap_mode(5)
  
  def activateWallTool(self):
    sender = self.sender()
    if sender :
      if self.last_mode :
        if self.last_mode[0] == sender : 
          sender.setStyleSheet(self.last_mode[1])
          sender.setFont(QFont(self.hunnin, 22))
          self.last_mode = None
          self.grid_map.setMap_mode(0)
          self.grid_map.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
          return 
        else :
          self.last_mode[0].setStyleSheet(self.last_mode[1])
          self.last_mode[0].setFont(QFont(self.hunnin, 22))
      currentStyleSheet = sender.styleSheet()
      newStyle = """
        QPushButton {
          color : white;
          background-color: #29e2ff;
        }
        QPushButton:hover {
          background-color: #29e2ff;
        }
      """
      sender.setStyleSheet(currentStyleSheet + newStyle)
      sender.setFont(QFont(self.calSans, 30))
      self.last_mode = [sender, currentStyleSheet]
      if sender == self.page2_addbutton :
        self.grid_map.setMap_mode(1)
        self.grid_map.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      else : 
        self.grid_map.setMap_mode(2)
        self.grid_map.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

  def changeEnemySkin(self):
    try :
      skin_filename, _ = QFileDialog.getOpenFileName(self,"Sélectionner l'image représentant un ennemi","","Images (*.png *.jpg *.jpeg)")
      QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
      image_to_ascii_by_color(skin_filename, "workingDir/enemy.txt", 70, 10)
      self.enemy_path = "workingDir/enemy.txt"
      self.grid_map.setEnemyImg(self.enemy_path)
      self.page3_infoskin.setText("Apparence des ennemis correctement définie")
      self.page3_infoskin.setStyleSheet("color : green;")
    except :
      pass
    QApplication.restoreOverrideCursor()

  def createNewPerso(self):
    if self.nb_perso < self.pers_limit :
      self.npc_dialog = NewNPC(self.addPersTable)
      self.npc_dialog.show()
    else :
      QMessageBox.warning(self, "Action impossible", "Désolé, vous avez atteint la limite de personnages.\nVeuillez supprimer un personnage existant avant de poursuivre.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

  def addPersTable(self, name, color):
    if name == "" :
      QMessageBox.warning(self, "Action impossible", "Malheureusement, un nom est requis pour votre personnage.\nMerci de le renseigner.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    elif name in [npc[0] for npc in self.NPCs] :
      QMessageBox.warning(self, "Action impossible", "Malheureusement, vous utilisez déjà ce nom pour un autre personnage.\nMerci d'en choisir un autre.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    elif color in self.pers_colors :
      QMessageBox.warning(self, "Action impossible", "Désolé, vous utilisez déjà cette couleur pour un autre personnage.\nMerci d'en utiliser une autre.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    else :
      if hasattr(self, 'npc_dialog') and self.npc_dialog.isVisible():
        self.npc_dialog.close()
      
      self.pers_colors.append(color)
      self.page4_table.setRowCount(self.nb_perso+1)
      pers_color = QColor(color)

      config_css = """
        QPushButton:hover {
          background-color: #c9c9c9;
        }
      """
      config_button = QPushButton("Configurer")
      config_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
      config_button.setCursor(Qt.CursorShape.PointingHandCursor)
      config_button.pressed.connect(self.switchRightSide)
      config_button.setFont(QFont(self.calSans, 18))
      config_button.setStyleSheet(config_css)
      config_button.setObjectName(name)

      name_item = QTableWidgetItem(name)
      name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.page4_table.setItem(self.nb_perso, 0, name_item)
      color_item = QTableWidgetItem()
      color_item.setBackground(pers_color)
      self.page4_table.setItem(self.nb_perso, 1, color_item)
      self.page4_table.setCellWidget(self.nb_perso, 2, config_button)
      self.nb_perso += 1
      self.NPCs.append([name, color])

  def deletePersoDialog(self):
    if self.NPCs == [] :
      QMessageBox.warning(self, "Action impossible", "Aucun personnage à supprimer.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    else :
      self.deleteNPCdialog = RemoveNPC(self)
      self.deleteNPCdialog.show()

  def deletePerso(self, name):
    if hasattr(self, 'deleteNPCdialog') and self.deleteNPCdialog.isVisible():
      self.deleteNPCdialog.close()
    for npc in self.NPCs :
      if npc[0] == name :
        self.NPCs.remove(npc)
        self.pers_colors.remove(npc[1])
        for position in self.grid_map.pos_NPCS :
          if position[1] == npc[1] :
            self.grid_map.pos_NPCS.remove(position)
            self.grid_map.update()
        row_to_remove = None
        for row in range(self.page4_table.rowCount()):
          item = self.page4_table.item(row, 0)
          if item and item.text() == name:
            row_to_remove = row
            break
        if row_to_remove is not None:
          self.page4_table.removeRow(row_to_remove)
          self.nb_perso -= 1
        break

  def selectNPCposition(self):
    self.switchRightSide(1)
    self.grid_map.setCursor(Qt.CursorShape.PointingHandCursor)
    self.grid_map.map_mode = 5

  def defineConversation(self):
    self.switchRightSide(2)

  def defineSkins(self):
    self.switchRightSide(3)
  
  def pos_given(self, position_transmitted) :
    if self.current_NPC_selected not in self.saved_NPCs:
      self.saved_NPCs[self.current_NPC_selected] = {}
    self.saved_NPCs[self.current_NPC_selected]["position"] = position_transmitted
    self.grid_map.map_mode = 0
    self.grid_map.setCursor(Qt.CursorShape.ArrowCursor)
    self.right_layout.setCurrentIndex(1)

  def skinGetter(self):
    sender = self.sender()
    filename, _ = QFileDialog.getOpenFileName(self,"Sélectionner l'image représentant votre personnage","","Images (*.png *.jpg *.jpeg)")
    if filename :
      os.makedirs("workingDir/NPCS/", exist_ok=True)
      if sender.text() == "Apparence 1 (obligatoire)" :
        image_to_ascii_by_color(filename,f"workingDir/NPCS/{self.current_NPC_selected}.txt", 100, 10, 1)
      elif sender.text() == "Apparence 2 (facultative)" :
        image_to_ascii_by_color(filename,f"workingDir/NPCS/{self.current_NPC_selected}.txt", 100, 10, 2)
      elif sender.text() == "Apparence 3 (facultative)" :
        image_to_ascii_by_color(filename,f"workingDir/NPCS/{self.current_NPC_selected}.txt", 100, 10, 3)
    
  def play(self):
    if self.grid_map.pos_player in [[], [-1.5,-1.5]] :
      QMessageBox.critical(self, "Exécution impossible", "Vous devez définir la case d'apparation de votre joueur avant de pouvoir lancer votre jeu.\nRendez-vous dans la section correspondante pour corriger cet incident.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    elif self.grid_map.pos_enemies != [] and self.enemy_path == None :
      QMessageBox.critical(self, "Exécution impossible", "Vous devez importer l'apparence graphique de vos ennemis avant de pouvoir lancer votre jeu.\nRendez-vous dans la section correspondante pour corriger cet incident.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)
    else :
      self.game = EmulatedTerminal()
      self.game.show()

  def openDialogWorkspace(self):
    print("\n--- Ouverture ---\n")
    if (self.current_NPC_selected in self.saved_NPCs) and "dialogWorkspace" in self.saved_NPCs[self.current_NPC_selected]:
      # Liste des ids uniques présents dans la zone de travail
      
      for bloc in self.saved_NPCs[self.current_NPC_selected]["dialogWorkspace"]:
        try :
          if hasattr(bloc, "deleted") and bloc.deleted:
            continue
          bloc.show()
          bloc.raise_()
        except RuntimeError :
          continue
      unique_ids_in_workspace = [bloc.id for bloc in self.bloc_working_zone.findChildren(Bloc) if (bloc.isVisibleTo(self.bloc_working_zone) and bloc.unique)]
      # Pour chaque bloc palette unique, on le cache seulement si son id est dans la zone de travail, sinon on le montre
      for i in range(self.pers_dialogue_layout.count()):
        widget = self.pers_dialogue_layout.itemAt(i).widget()
        if widget is not None and getattr(widget, "unique", False):
          if widget.id in unique_ids_in_workspace:
            widget.hide()
    else :
      for i in range(self.pers_dialogue_layout.count()):
        widget = self.pers_dialogue_layout.itemAt(i).widget()
        if widget is not None :   
          widget.show()
      
  def saveDialogWorkspace(self):
    save = []
    blocs = self.bloc_working_zone.findChildren(Bloc)
    print("\n--- Fermeture ---\n")
    print("Blocs trouvés :", blocs)
    print("Blocs visibles :", [bloc for bloc in blocs if bloc.isVisibleTo(self.bloc_working_zone)])
    for bloc in blocs:
      if bloc.isVisibleTo(self.bloc_working_zone) :
        save.append(bloc)
        bloc.hide()
    if save:
      if self.current_NPC_selected not in self.saved_NPCs:
        self.saved_NPCs[self.current_NPC_selected] = {}
      self.saved_NPCs[self.current_NPC_selected]["dialogWorkspace"] = save

  def createActions(self):
    self.quit_act = QAction("&Quitter")
    self.quit_act.setShortcut("Ctrl+Q")
    self.quit_act.triggered.connect(self.close)

    self.exec_act = QAction("&Démarrer votre jeu")
    self.exec_act.setShortcut("Ctrl+E")
    self.exec_act.triggered.connect(self.play)

  def createMenu(self):
    file_menu = self.menuBar().addMenu("Fichier")
    file_menu.addAction(self.quit_act)

    edit_menu = self.menuBar().addMenu("Edition")
    exec_menu = self.menuBar().addMenu("Exécution")
    exec_menu.addAction(self.exec_act)
    help_menu = self.menuBar().addMenu("Aide")

  def maintainSpacingLayout(self):
    self.main_layout.setSpacing(int(self.width() * 0.01))

  def resizeTitles(self):
    responsive_font_size = min(self.width()//24, self.height()//24)
    self.title_map.setFont(QFont(self.calSans, responsive_font_size))
    self.title_tools.setFont(QFont(self.calSans, responsive_font_size))

  def resizeReleaseZone(self):
    top_left = self.bloc_working_zone.mapTo(self, self.bloc_working_zone.rect().topLeft())
    bottom_right = self.bloc_working_zone.mapTo(self, self.bloc_working_zone.rect().bottomRight())
    self.bloc_zone = [(top_left.x()+2, top_left.y()), (bottom_right.x()-2, bottom_right.y()-100)]

  def resizeEvent(self, event):
    if hasattr(self, 'main_layout'):
      self.maintainSpacingLayout()
    if hasattr(self, 'title_map'):
      self.resizeTitles()
    if hasattr(self, "bloc_working_zone"):
      self.resizeReleaseZone()
    super().resizeEvent(event)
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec())