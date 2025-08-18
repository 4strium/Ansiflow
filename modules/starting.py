import sys, json, os, zipfile, shutil
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QCursor, QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from modules.newProject import NewProject
from modules.otherTools import translation

class StartWindow(QWidget):
  finished = pyqtSignal()

  def __init__(self):
    super().__init__()
    self.__startup_finished = False
    self.__map_size = -1
    self.user_language = "fr"  # Défaut français
    self.initializeUI()

  def getStartup_finished(self):
    return self.__startup_finished
  
  def setStartup_finished(self, nval):
    self.__startup_finished = nval

  def getMap_size(self):
    return self.__map_size
  
  def setMap_size(self, nsize):
    self.__map_size = nsize

  def initializeUI(self):
    self.setWindowTitle(translation("starting_window_title", self.user_language))
    self.setMinimumSize(800,500)
    self.resize(1200, 700)
    self.setStyleSheet("background-color: white;")
    try:
      self.setWindowIcon(QIcon("images/ansiflow-icon.png"))
    except Exception:
      pass

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/CalSans.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.calSans = font_families[0]
    else:
      self.calSans = "Arial"

    self.setUpWindow()
    self.show()

  def setUpWindow(self):
    image_splash = "images/ansiflow.png"

    try :
      with open(image_splash):
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(image_splash)
        img_width = int(self.width() * 0.4)
        img_height = int(self.height() * 0.2)
        self.pixmap_new_scale = self.pixmap.scaled(img_width, img_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(self.pixmap_new_scale)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    except FileNotFoundError as error:
      print("Image not found...")

    # Boutons de sélection de langue
    self.language_layout = QHBoxLayout()
    self.language_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.language_layout.setSpacing(20)
    
    # Bouton français
    self.french_button = QPushButton()
    self.french_pixmap = QPixmap("images/france.png")
    self.french_scaled = self.french_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    self.french_button.setIcon(QIcon(self.french_scaled))
    self.french_button.setIconSize(self.french_scaled.size())
    self.french_button.setFixedSize(80, 80)
    self.french_button.clicked.connect(lambda: self.setLanguage("fr"))
    self.french_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
    # Bouton anglais
    self.english_button = QPushButton()
    self.english_pixmap = QPixmap("images/anglais.png")
    self.english_scaled = self.english_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    self.english_button.setIcon(QIcon(self.english_scaled))
    self.english_button.setIconSize(self.english_scaled.size())
    self.english_button.setFixedSize(80, 80)
    self.english_button.clicked.connect(lambda: self.setLanguage("en"))
    self.english_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
    self.language_layout.addWidget(self.french_button)
    self.language_layout.addWidget(self.english_button)
    
    # Mettre à jour les styles selon la langue par défaut
    self.updateLanguageButtonStyles()

    self.new_project_button = QPushButton(translation("starting_new_project", self.user_language))
    self.charge_project_button = QPushButton(translation("starting_load_project", self.user_language))
    self.new_project_button.clicked.connect(self.createPrimaryContent)
    self.charge_project_button.clicked.connect(self.openPreviousProject)

    self.buttons_layout = QHBoxLayout()
    self.buttons_layout.addWidget(self.new_project_button)
    self.buttons_layout.addWidget(self.charge_project_button)
    self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.buttons_layout.setSpacing(img_width//8)

    self.new_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.charge_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    btn_css = """
      QPushButton {
        border-radius: 10%;
        background-color: #13d6df;
        color : white;
      }
      QPushButton:hover {
        background-color: white;
        color : #13d6df;
      }
    """

    self.new_project_button.setStyleSheet(btn_css)
    self.new_project_button.setFont(QFont(self.calSans, 48))
    self.new_project_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.charge_project_button.setStyleSheet(btn_css)
    self.charge_project_button.setFont(QFont(self.calSans, 48))
    self.charge_project_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    introductive_content = QVBoxLayout()
    introductive_content.addWidget(self.image_label)
    introductive_content.addLayout(self.language_layout)
    introductive_content.addLayout(self.buttons_layout)
    introductive_content.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.setLayout(introductive_content)

  def setLanguage(self, language):
    """Change la langue et met à jour l'interface"""
    self.user_language = language
    self.updateLanguageButtonStyles()
    self.updateTexts()
  
  def updateLanguageButtonStyles(self):
    """Met à jour les styles des boutons de langue selon la sélection"""
    selected_style = """
      QPushButton {
        border: 4px solid #13d6df;
        border-radius: 8px;
        background-color: rgba(5, 241, 247, 0.2);
      }
      QPushButton:hover {
        background-color: rgba(5, 241, 247, 0.4);
      }
    """
    
    default_style = """
      QPushButton {
        border: 2px solid transparent;
        border-radius: 8px;
        background-color: transparent;
      }
      QPushButton:hover {
        border: 2px solid #13d6df;
        background-color: rgba(5, 241, 247, 0.1);
      }
    """
    
    if self.user_language == "fr":
      self.french_button.setStyleSheet(selected_style)
      self.english_button.setStyleSheet(default_style)
    else:
      self.english_button.setStyleSheet(selected_style)
      self.french_button.setStyleSheet(default_style)
  
  def updateTexts(self):
    """Met à jour tous les textes selon la langue sélectionnée"""
    self.setWindowTitle(translation("starting_window_title", self.user_language))
    self.new_project_button.setText(translation("starting_new_project", self.user_language))
    self.charge_project_button.setText(translation("starting_load_project", self.user_language))
    # Forcer une mise à jour du layout pour les nouveaux textes
    self.update()


  def createPrimaryContent(self):
    self.new_project_dialog = NewProject(self.user_language)
    self.new_project_dialog.finished.connect(self.handleNewProjectFinished)
    self.new_project_dialog.show()

  def handleNewProjectFinished(self):
    if self.new_project_dialog.getSetup_finished():
      self.setMap_size(self.new_project_dialog.getSize_choosen())
      self.setStartup_finished(True)
      self.finished.emit()  

  def openPreviousProject(self):
    project_compressed, _ = QFileDialog.getOpenFileName(self,translation("starting_open_file_title", self.user_language),"","*.ansiflow")
    if project_compressed :

      os.makedirs("workingDir", exist_ok=True)

      for filename in os.listdir("workingDir"):
        file_path = os.path.join("workingDir", filename)
        if os.path.isfile(file_path):
          os.remove(file_path)
        elif os.path.isdir(file_path):
          shutil.rmtree(file_path)

      with zipfile.ZipFile(project_compressed, 'r') as zip_content:
        zip_content.extractall("workingDir/")    
      
      with open("workingDir/data.json", 'r', encoding="utf-8") as f:
        json_data = json.load(f)
      self.setMap_size(len(json_data["map"][0]))
      self.setStartup_finished(True)
      self.finished.emit()

  def resizeSplashImage(self):
    img_width = int(self.width() * 0.8)
    img_height = int(self.height() * 0.6)
    self.pixmap_new_scale = self.pixmap.scaled(img_width, img_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    self.image_label.setPixmap(self.pixmap_new_scale)

  def resizeIntroButtons(self):
    individual_btn_width = (self.image_label.pixmap().width()//2)
    button_height = int(self.height() * 0.15)

    responsive_font_size = min(button_height//3, individual_btn_width//(len(self.charge_project_button.text())-2))
    self.charge_project_button.setFont(QFont(self.calSans, responsive_font_size))
    self.new_project_button.setFont(QFont(self.calSans, responsive_font_size))
    self.new_project_button.setFixedSize(individual_btn_width, button_height)
    self.charge_project_button.setFixedSize(individual_btn_width, button_height)
    self.buttons_layout.setSpacing(individual_btn_width//8)

  def resizeEvent(self, event):
    self.resizeSplashImage()
    self.resizeIntroButtons()
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = StartWindow()
  sys.exit(app.exec())