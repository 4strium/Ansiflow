import json
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QComboBox
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from PyQt6.QtCore import Qt
from modules.otherTools import translation

class parametersDialog(QDialog) :
  def __init__(self, mainApp):
    super().__init__()
    self.setModal(True)
    self.main_app = mainApp
    self.user_language = mainApp.user_language

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(400,350)
    self.setWindowTitle(translation("parameters_window_title", self.user_language))

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    self.new_name_label = QLabel(translation("parameters_project_name", self.user_language))
    self.new_name_label.setFont(QFont(self.hunnin, 14))
    self.new_name = QLineEdit(self)
    self.new_name.setFont(QFont(self.hunnin, 14))
    self.new_name.setText(self.main_app.game_name)
    self.new_name.setMaxLength(20)
    self.new_name.setFixedWidth(200)
    
    # Sélecteur de langue
    self.language_label = QLabel(translation("parameters_language_label", self.user_language))
    self.language_label.setFont(QFont(self.hunnin, 14))
    
    self.language_combo = QComboBox(self)
    self.language_combo.setFont(QFont(self.hunnin, 14))
    self.language_combo.addItem(translation("parameters_language_french", self.user_language), "fr")
    self.language_combo.addItem(translation("parameters_language_english", self.user_language), "en")
    
    # Définir la langue actuelle comme sélectionnée
    current_index = 0 if self.user_language == "fr" else 1
    self.language_combo.setCurrentIndex(current_index)
    self.language_combo.setFixedWidth(200)
    
    self.validation = QPushButton(translation("parameters_confirm", self.user_language))
    self.validation.setFont(QFont(self.hunnin, 14))
    self.validation.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    self.validation.clicked.connect(self.entryConfirmation)

    # Layout configuration :
    blankspace = QWidget()
    spacing = QHBoxLayout()
    spacing.addWidget(blankspace, stretch=2)
    spacing.addWidget(self.validation, stretch=1)

    final_layout = QVBoxLayout()
    final_layout.addWidget(self.new_name_label)
    final_layout.addWidget(self.new_name)
    final_layout.addWidget(self.language_label)
    final_layout.addWidget(self.language_combo)
    final_layout.addStretch()
    final_layout.addLayout(spacing)

    self.setLayout(final_layout)

  def entryConfirmation(self):
    if self.new_name.text().strip() == "":
      QMessageBox.warning(self, translation("parameters_error_title", self.user_language), translation("parameters_error_empty_name", self.user_language))
      return
    
    # Récupérer la nouvelle langue sélectionnée
    new_language = self.language_combo.currentData()
    language_changed = new_language != self.user_language
      
    self.main_app.game_name = self.new_name.text()
    
    # Mettre à jour la langue dans l'application principale
    if language_changed:
      self.main_app.user_language = new_language

    try :
      with open(self.main_app.data_file, "r", encoding="utf-8") as f :
        json_data = json.load(f)

      json_data["name"] = self.main_app.game_name
      
      with open(self.main_app.data_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    except FileNotFoundError:
      QMessageBox.critical(self, translation("parameters_error_title", self.user_language), f"{self.main_app.data_file}{translation('parameters_error_file_not_found', self.user_language)}")
    except json.JSONDecodeError:
      QMessageBox.critical(self, translation("parameters_error_title", self.user_language), f"{self.main_app.data_file}{translation('parameters_error_invalid_json', self.user_language)}")
    except Exception as e:
      QMessageBox.critical(self, translation("parameters_error_title", self.user_language), f"{translation('parameters_error_modify_json', self.user_language)}{str(e)}")
    
    # Mettre à jour l'interface si la langue a changé
    if language_changed:
      self.main_app.updateInterfaceTexts()
    
    self.accept()