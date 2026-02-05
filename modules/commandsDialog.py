from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QFontDatabase, QCursor, QIcon
from PyQt6.QtCore import Qt
from modules.otherTools import translation

class CommandsDialog(QDialog):
  def __init__(self, main_app):
    super().__init__()
    self.setModal(True)
    self.main_app = main_app
    self.user_language = main_app.user_language
    self.initializeUI()

  def initializeUI(self):
    self.setWindowTitle(translation("commands_dialog_title", self.user_language))
    self.setFixedSize(500, 400)
    try:
      self.setWindowIcon(QIcon("images/ansiflow-icon.png"))
    except Exception:
      pass

    # Police
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    families = QFontDatabase.applicationFontFamilies(font_id)
    if families:
      self.dialog_font = families[0]
    else:
      self.dialog_font = "Arial"

    layout = QVBoxLayout()

    header = QLabel(translation("commands_dialog_header", self.user_language))
    header.setFont(QFont(self.dialog_font, 20))
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)

    move = QLabel(translation("commands_dialog_move", self.user_language))
    rotate = QLabel(translation("commands_dialog_rotate", self.user_language))
    shoot = QLabel(translation("commands_dialog_shoot", self.user_language))
    quit_game = QLabel(translation("commands_dialog_quit", self.user_language))

    for lbl in (move, rotate, shoot, quit_game):
      lbl.setFont(QFont(self.dialog_font, 16))
      lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)

    self.ok_btn = QPushButton(translation("commands_dialog_ok", self.user_language))
    self.ok_btn.setFont(QFont(self.dialog_font, 18))
    self.ok_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.ok_btn.clicked.connect(self.accept)

    layout.addWidget(header)
    layout.addSpacing(10)
    layout.addWidget(move)
    layout.addWidget(rotate)
    layout.addWidget(shoot)
    layout.addWidget(quit_game)
    layout.addStretch()
    layout.addWidget(self.ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    self.setLayout(layout)

  def updateTexts(self):
    self.setWindowTitle(translation("commands_dialog_title", self.user_language))
    # Could be expanded if dynamic language change while open is required.
