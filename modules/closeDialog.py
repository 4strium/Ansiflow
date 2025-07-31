from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from PyQt6.QtCore import Qt

class closeDialog(QDialog) :
  def __init__(self, mainApp, event):
    super().__init__()
    self.setModal(True)
    self.main_app = mainApp
    self.app_event = event

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(800,120)
    self.setWindowTitle("Fermeture de l'application")

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    self.warning_text = QLabel("Souhaitez-vous enregistrer votre projet avant de quitter l'application ?")
    self.warning_text.setFont(QFont(self.hunnin, 14))
    
    self.yes_save = QPushButton("Oui")
    self.yes_save.setFont(QFont(self.hunnin, 14))
    self.yes_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.yes_save.clicked.connect(self.dialogEvent)

    self.no_save = QPushButton("Non")
    self.no_save.setFont(QFont(self.hunnin, 14))
    self.no_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.no_save.clicked.connect(self.dialogEvent)

    self.cancel_save = QPushButton("Annuler")
    self.cancel_save.setFont(QFont(self.hunnin, 14))
    self.cancel_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.cancel_save.clicked.connect(self.dialogEvent)

    # Layout configuration :
    blankspace = QWidget()
    spacing = QHBoxLayout()
    spacing.addWidget(blankspace, stretch=1)
    spacing.addWidget(self.yes_save, stretch=1)
    spacing.addWidget(self.no_save, stretch=1)
    spacing.addWidget(self.cancel_save, stretch=1)

    final_layout = QVBoxLayout()
    final_layout.addWidget(self.warning_text)
    final_layout.addLayout(spacing)

    self.setLayout(final_layout)

  def dialogEvent(self):
    sender = self.sender()
    if sender :
      if sender.text() == "Oui" :
        self.main_app.save()
        self.accept()
      elif sender.text() == "Non" :
        self.accept()
      elif sender.text() == "Annuler" :
        self.reject()