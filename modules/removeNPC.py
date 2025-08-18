from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QComboBox
from PyQt6.QtGui import QFont, QPixmap, QCursor, QIcon
from PyQt6.QtCore import Qt

class RemoveNPC(QDialog):
  def __init__(self, app):
    super().__init__()
    self.setModal(True)
    self.main_app = app
    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(400,500)
    self.setWindowTitle("Suppression d'un personnage...")
    try:
      self.setWindowIcon(QIcon("images/ansiflow-icon.png"))
    except Exception:
      pass
    self.setUpWindow()

  def setUpWindow(self):
    suppression_icon = "images/bin.png"

    try :
      with open(suppression_icon):
        suppr_label = QLabel(self)
        pixmap = QPixmap(suppression_icon)
        suppr_label.setPixmap(pixmap)
        suppr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    except FileNotFoundError :
      pass

    name_label = QLabel("Personnage à supprimer :", self)
    name_label.setFont(QFont(self.main_app.hunnin, 20))
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.combo_name = QComboBox(self)
    self.combo_name.setFont(QFont(self.main_app.hunnin, 20))
    self.combo_name.addItems([npc[0] for npc in self.main_app.NPCs])

    name_layout = QVBoxLayout()
    name_layout.addWidget(name_label)
    name_layout.addWidget(self.combo_name)

    confirm_btn = QPushButton("Valider")
    confirm_btn.setFont(QFont(self.main_app.hunnin, 24))
    confirm_btn.setMinimumHeight(80)
    confirm_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    confirm_btn.clicked.connect(lambda: self.main_app.deletePerso(self.combo_name.currentText()))

    self.suppression_layout = QVBoxLayout()
    self.suppression_layout.addWidget(suppr_label)
    self.suppression_layout.addStretch(20)
    self.suppression_layout.addLayout(name_layout)
    self.suppression_layout.addStretch(20)
    self.suppression_layout.addWidget(confirm_btn)

    self.setLayout(self.suppression_layout)