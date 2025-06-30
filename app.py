import sys
import zipfile
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from PyQt6.QtCore import Qt
from modules.newProject import NewProject

class MainWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.initializeUI()

  def initializeUI(self):
    self.setWindowTitle("Patate - The 3D ASCII Game Engine")
    self.setMinimumSize(800,500)
    self.resize(1200, 700)
    self.setStyleSheet("background-color: #876acf;")

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
    image_splash = "images/splashscreen.jpg"

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

    self.new_project_button = QPushButton("Nouveau Projet")
    self.charge_project_button = QPushButton("Charger Projet")
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
        background-color: #05f1f7;
        color : white;
      }
      QPushButton:hover {
        background-color: white;
        color : #05f1f7;
      }
    """

    self.new_project_button.setStyleSheet(btn_css)
    self.new_project_button.setFont(QFont(self.calSans, 48))
    self.charge_project_button.setStyleSheet(btn_css)
    self.charge_project_button.setFont(QFont(self.calSans, 48))

    introductive_content = QVBoxLayout()
    introductive_content.addWidget(self.image_label)
    introductive_content.addLayout(self.buttons_layout)

    introductive_content.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.setLayout(introductive_content)

  def createPrimaryContent(self):
    self.new_project_dialog = NewProject()
    self.new_project_dialog.show()
    self.switchWorkWindow()

  def switchWorkWindow(self):
    pass

  def openPreviousProject(self):
    project_compressed, _ = QFileDialog.getOpenFileName(self,"Ouvrir un fichier de projet","","*.zip")
    if project_compressed :
      with zipfile.ZipFile(project_compressed, 'r') as zip_content:
        zip_content.extractall("workingDir/")    
  
      self.switchWorkWindow()

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
  window = MainWindow()
  sys.exit(app.exec())