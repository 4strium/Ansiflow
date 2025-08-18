from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont, QFontDatabase, QCursor, QIcon
from PyQt6.QtCore import Qt
from modules.otherTools import translation

class NPCresponsesDialog(QDialog) :
  def __init__(self, bloc, nb_resp):
    super().__init__()
    self.setModal(True)
    self.savingPort = bloc.storage
    self.nb_resp = nb_resp
    self.user_language = "fr"  # Défaut français

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(800,self.nb_resp*100)
    self.setWindowTitle(translation("npc_responses_dialog_title", self.user_language))
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

    final_layout = QVBoxLayout()

    self.resp1_label = QLabel(translation("npc_responses_response1", self.user_language))
    self.resp1_label.setFont(QFont(self.hunnin, 14))
    self.resp1_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
    self.input_text_resp1 = QLineEdit(self)
    self.input_text_resp1.setFont(QFont(self.hunnin, 16))
    self.input_text_resp1.setMaxLength(78)
    if self.savingPort[1] :
      self.input_text_resp1.setText(self.savingPort[1])
    layout_resp1 = QVBoxLayout()
    layout_resp1.setContentsMargins(0,0,0,0)
    layout_resp1.setSpacing(0)
    layout_resp1.addWidget(self.resp1_label)
    layout_resp1.addWidget(self.input_text_resp1)
    final_layout.addLayout(layout_resp1)

    self.resp2_label = QLabel(translation("npc_responses_response2", self.user_language))
    self.resp2_label.setFont(QFont(self.hunnin, 14))
    self.resp2_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
    self.input_text_resp2 = QLineEdit(self)
    self.input_text_resp2.setFont(QFont(self.hunnin, 16))
    self.input_text_resp2.setMaxLength(78)
    if self.savingPort[2] :
      self.input_text_resp2.setText(self.savingPort[2])
    layout_resp2 = QVBoxLayout()
    layout_resp2.setSpacing(0)
    layout_resp2.setContentsMargins(0,0,0,0)
    layout_resp2.addWidget(self.resp2_label)
    layout_resp2.addWidget(self.input_text_resp2)
    final_layout.addLayout(layout_resp2)

    if self.nb_resp == 3 :
      self.resp3_label = QLabel(translation("npc_responses_response3", self.user_language))
      self.resp3_label.setFont(QFont(self.hunnin, 14))
      self.resp3_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
      self.input_text_resp3 = QLineEdit(self)
      self.input_text_resp3.setFont(QFont(self.hunnin, 16))
      self.input_text_resp3.setMaxLength(78)
      layout_resp3 = QVBoxLayout()
      layout_resp3.setSpacing(0)
      layout_resp3.setContentsMargins(0,0,0,0)
      layout_resp3.addWidget(self.resp3_label)
      layout_resp3.addWidget(self.input_text_resp3)
      final_layout.addLayout(layout_resp3)
    
    self.validation = QPushButton(translation("npc_responses_confirm", self.user_language))
    self.validation.setFont(QFont(self.hunnin, 14))
    self.validation.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.validation.clicked.connect(self.entryConfirmation)

    # Layout configuration :
    blankspace = QWidget()
    spacing = QHBoxLayout()
    spacing.addWidget(blankspace, stretch=2)
    spacing.addWidget(self.validation, stretch=1)

    final_layout.addLayout(spacing)
    self.setLayout(final_layout)

  def entryConfirmation(self):
    if self.input_text_resp1.text().strip() == "" or self.input_text_resp2.text().strip() == "":
      QMessageBox.warning(self, translation("npc_responses_error_title", self.user_language), translation("npc_responses_error_empty", self.user_language))
      return
  
    self.savingPort[1] = self.input_text_resp1.text()
    self.savingPort[2] = self.input_text_resp2.text()

    if self.nb_resp == 3 :
      if self.input_text_resp3.text().strip() == "" :
        QMessageBox.warning(self, translation("npc_responses_error_title", self.user_language), translation("npc_responses_error_empty", self.user_language))
        return
      self.savingPort[3] = self.input_text_resp3.text()
    
    self.accept()