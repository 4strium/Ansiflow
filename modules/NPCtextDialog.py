from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase, QCursor, QIcon
from PyQt6.QtCore import Qt
from modules.otherTools import translation

class NPCtextDialog(QDialog) :
  def __init__(self, bloc):
    super().__init__()
    self.setModal(True)
    self.savingBloc = bloc
    self.user_language = "fr"  # Défaut français

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(800,100)
    self.setWindowTitle(translation("npc_text_dialog_title", self.user_language))
    try:
      self.setWindowIcon(QIcon("images/ansiflow-icon.png"))
    except Exception:
      pass

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    self.input_text = QLineEdit(self)
    self.input_text.setFont(QFont(self.hunnin, 16))
    self.input_text.setMaxLength(78)
    
    if self.savingBloc.storage[0] :
      self.input_text.setText(self.savingBloc.storage[0])

    self.validation = QPushButton(translation("npc_text_dialog_confirm", self.user_language))
    self.validation.setFont(QFont(self.hunnin, 14))
    self.validation.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.validation.clicked.connect(self.entryConfirmation)

    # Layout configuration :
    blankspace = QWidget()
    spacing = QHBoxLayout()
    spacing.addWidget(blankspace, stretch=2)
    spacing.addWidget(self.validation, stretch=1)

    final_layout = QVBoxLayout()
    final_layout.addWidget(self.input_text)
    final_layout.addLayout(spacing)

    self.setLayout(final_layout)

  def entryConfirmation(self):
    if self.input_text.text().strip() == "":
      QMessageBox.warning(self, translation("npc_text_dialog_error_title", self.user_language), translation("npc_text_dialog_error_empty", self.user_language))
      return
      
    self.savingBloc.storage[0] = self.input_text.text()
    
    self.accept()