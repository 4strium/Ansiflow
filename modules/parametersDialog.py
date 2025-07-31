import json
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase, QCursor
from PyQt6.QtCore import Qt

class parametersDialog(QDialog) :
  def __init__(self, mainApp):
    super().__init__()
    self.setModal(True)
    self.main_app = mainApp

    self.initializeUI()

  def initializeUI(self):
    self.setFixedSize(400,300)
    self.setWindowTitle("Configuration de votre projet")

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/Huninn.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.hunnin = font_families[0]
    else:
      self.hunnin = "Arial"

    self.setUpWindow()

  def setUpWindow(self):
    self.new_name_label = QLabel(" Nom du projet :")
    self.new_name_label.setFont(QFont(self.hunnin, 14))
    self.new_name = QLineEdit(self)
    self.new_name.setFont(QFont(self.hunnin, 14))
    self.new_name.setText(self.main_app.game_name)
    self.new_name.setMaxLength(20)
    self.new_name.setFixedWidth(200)
    
    self.validation = QPushButton("Confirmer")
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
    final_layout.addStretch()
    final_layout.addLayout(spacing)

    self.setLayout(final_layout)

  def entryConfirmation(self):
    if self.new_name.text().strip() == "":
      QMessageBox.warning(self, "Erreur", "Le nom du jeu ne peut pas être vide ou seulement composé d'espaces.")
      return
      
    self.main_app.game_name = self.new_name.text()

    try :
      with open(self.main_app.data_file, "r", encoding="utf-8") as f :
        json_data = json.load(f)

      json_data["name"] = self.main_app.game_name
      
      with open(self.main_app.data_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    except FileNotFoundError:
      QMessageBox.critical(self, "Erreur", f"Le fichier {self.main_app.data_file} n'a pas été trouvé.")
    except json.JSONDecodeError:
      QMessageBox.critical(self, "Erreur", f"Le fichier {self.main_app.data_file} n'est pas un JSON valide.")
    except Exception as e:
      QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la modification du fichier JSON: {str(e)}")
    
    self.accept()