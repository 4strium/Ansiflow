from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from PyQt6.QtCore import Qt
from modules.otherTools import translation

class closeDialog(QDialog) :
  def __init__(self, mainApp, event):
    super().__init__()
    self.setModal(True)
    self.main_app = mainApp
    self.app_event = event
    self.user_language = mainApp.user_language

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(800,120)
    self.setWindowTitle(translation("close_dialog_title", self.user_language))

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    self.warning_text = QLabel(translation("close_dialog_question", self.user_language))
    self.warning_text.setFont(QFont(self.hunnin, 14))
    
    self.yes_save = QPushButton(translation("close_dialog_yes", self.user_language))
    self.yes_save.setFont(QFont(self.hunnin, 14))
    self.yes_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.yes_save.clicked.connect(self.dialogEvent)

    self.no_save = QPushButton(translation("close_dialog_no", self.user_language))
    self.no_save.setFont(QFont(self.hunnin, 14))
    self.no_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.no_save.clicked.connect(self.dialogEvent)

    self.cancel_save = QPushButton(translation("close_dialog_cancel", self.user_language))
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
      if sender.text() == translation("close_dialog_yes", self.user_language) :
        self.main_app.save()
        self.accept()
      elif sender.text() == translation("close_dialog_no", self.user_language) :
        self.accept()
      elif sender.text() == translation("close_dialog_cancel", self.user_language) :
        self.reject()