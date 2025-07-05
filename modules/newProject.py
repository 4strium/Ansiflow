import os, json
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase, QCursor
from PyQt6.QtCore import Qt

class NewProject(QDialog):
  def __init__(self):
    super().__init__()
    self.setModal(True)
    self.__setup_finished = False
    self.__size_choosen = -1
    self.initializeUI()

  def getSetup_finished(self):
    return self.__setup_finished

  def setSetup_finished(self, nval):
    self.__setup_finished = nval

  def getSize_choosen(self):
    return self.__size_choosen

  def setSize_choosen(self, nsize):
    self.__size_choosen = nsize

  def initializeUI(self):
    self.setFixedSize(450,600)
    self.setWindowTitle("Nouveau projet...")

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    creation_icon = "images/prototype.png"

    try :
      with open(creation_icon):
        crea_label = QLabel(self)
        pixmap = QPixmap(creation_icon)
        crea_label.setPixmap(pixmap)
        crea_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    except FileNotFoundError :
      pass

    name_label = QLabel("Nom de votre projet :", self)
    name_label.setFont(QFont(self.hunnin, 24))
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.name_linedit = QLineEdit(self)
    self.name_linedit.setMaxLength(15)
    self.name_linedit.setFont(QFont(self.hunnin, 18))
    self.name_linedit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    name_layout = QVBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(self.name_linedit)
    name_layout.setSpacing(2)

    size_label = QLabel("Taille de la carte :", self)
    size_label.setFont(QFont(self.hunnin, 24))
    size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    sizes_availables = ["8x8", "16x16", "32x32", "64x64"]
    self.ddmenu_size = QComboBox()
    self.ddmenu_size.addItems(sizes_availables)
    self.ddmenu_size.setFont(QFont(self.hunnin, 18))
    self.ddmenu_size.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    size_layout = QVBoxLayout()
    size_layout.addWidget(size_label)
    size_layout.addWidget(self.ddmenu_size)
    size_layout.setSpacing(2)

    confirm_btn = QPushButton("Valider")
    confirm_btn.setFont(QFont(self.hunnin, 24))
    confirm_btn.setMinimumHeight(80)
    confirm_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    confirm_btn.clicked.connect(self.createDataFile)

    self.creation_layout = QVBoxLayout()
    self.creation_layout.addWidget(crea_label)
    self.creation_layout.addStretch(20)
    self.creation_layout.addLayout(name_layout)
    self.creation_layout.addStretch(20)
    self.creation_layout.addLayout(size_layout)
    self.creation_layout.addStretch(50)
    self.creation_layout.addWidget(confirm_btn)

    self.setLayout(self.creation_layout)

  def createDataFile(self):
    if self.name_linedit.text():
      details = {"name": self.name_linedit.text(), "player": [-1, -1], "Enemy": []}

      map_data = []
      self.setSize_choosen(int((self.ddmenu_size.currentText()).split("x")[0]))

      for i in range(self.getSize_choosen()):
        line_tmp = []
        for j in range(self.getSize_choosen()):
          if i in [0, self.getSize_choosen()-1] or j in [0,self.getSize_choosen()-1] :
            line_tmp.append(1)
          else :
            line_tmp.append(0)
        map_data.append(line_tmp)
      
      details["map"] = map_data
      
      os.makedirs("workingDir", exist_ok=True)
      with open("workingDir/data.json", "w", encoding="utf-8") as f:
        # Utilisez dump, pas dumps, et ajoutez indent pour l'indentation
        json.dump(details, f, indent=2, sort_keys=False, ensure_ascii=False)
      
      self.setSetup_finished(True)
      self.close()
    else :
      QMessageBox.warning(self, "Nom de projet invalide", "Un nom de projet est requis pour la suite du processus.\nMerci de bien vouloir le renseigner.", QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)