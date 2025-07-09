from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QFontDatabase, QCursor
from PyQt6.QtCore import Qt

class NewNPC(QDialog):
  def __init__(self, appFunc):
    super().__init__()
    self.setModal(True)
    self.__name_choosen = ""
    self.triggered_func = appFunc
    self.initializeUI()

  def getDialog_finished(self):
    return self.__dialog_finished

  def setDialog_finished(self, nval):
    self.__dialog_finished = nval

  def getName_choosen(self):
    return self.__name_choosen

  def setName_choosen(self, nname):
    self.__name_choosen = nname

  def initializeUI(self):
    self.setFixedSize(400,600)
    self.setWindowTitle("Nouveau personnage...")

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

    name_label = QLabel("Nom de votre personnage :", self)
    name_label.setFont(QFont(self.hunnin, 20))
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.name_linedit = QLineEdit(self)
    self.name_linedit.setMaxLength(15)
    self.name_linedit.setFont(QFont(self.hunnin, 18))
    self.name_linedit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    name_layout = QVBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(self.name_linedit)
    name_layout.setSpacing(2)

    color_label = QLabel("Couleur représentative :", self)
    color_label.setFont(QFont(self.hunnin, 20))
    color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.color_combo = QComboBox(self)
    self.color_combo.setFont(QFont(self.hunnin, 16))
    colors = [
      ("Rouge", "#FF0000"),
      ("Marron", "#8B4513"),
      ("Orange", "#FFA500"),
      ("Jaune", "#FFFF00"),
      ("Bleu", "#0000FF"),
      ("Cyan", "#00FFFF"),
      ("Magenta", "#FF00FF"),
      ("Gris", "#888888")
    ]
    for name, hexcode in colors:
      self.color_combo.addItem(name, hexcode)
    self.color_combo.setCurrentIndex(0)
    self.color_combo.currentIndexChanged.connect(
      lambda idx: setattr(self, "_NewNPC__color_choosen", self.color_combo.itemData(idx))
    )

    color_layout = QVBoxLayout()
    color_layout.addWidget(color_label)
    color_layout.addWidget(self.color_combo)
    color_layout.setSpacing(2)

    confirm_btn = QPushButton("Valider")
    confirm_btn.setFont(QFont(self.hunnin, 24))
    confirm_btn.setMinimumHeight(80)
    confirm_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    confirm_btn.clicked.connect(lambda: self.triggered_func(self.name_linedit.text(), self.color_combo.currentData()))

    self.creation_layout = QVBoxLayout()
    self.creation_layout.addWidget(crea_label)
    self.creation_layout.addStretch(20)
    self.creation_layout.addLayout(name_layout)
    self.creation_layout.addStretch(20)
    self.creation_layout.addLayout(color_layout)
    self.creation_layout.addStretch(50)
    self.creation_layout.addWidget(confirm_btn)

    self.setLayout(self.creation_layout)