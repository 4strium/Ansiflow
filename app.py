import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QAction
from PyQt6.QtCore import Qt
from modules.starting import StartWindow

class MainWindow(QMainWindow):

  def __init__(self):
    super().__init__()
    self.startup()

  def startup(self) :
    self.sw = StartWindow()
    self.sw.show()
    self.sw.finished.connect(self.handleStartupFinished)

  def handleStartupFinished(self):
    if self.sw.getStartup_finished() :
      self.sw.close()
      self.initializeUI()

  def initializeUI(self):
    self.setWindowTitle("Patate - The 3D ASCII Game Engine")
    self.setMinimumSize(800,500)
    self.showMaximized()

    # Load the custom font
    font_id = QFontDatabase.addApplicationFont("fonts/CalSans.ttf")
    font_families = QFontDatabase.applicationFontFamilies(font_id)

    if font_families:
      self.calSans = font_families[0]
    else:
      self.calSans = "Arial"

    self.setUpWindow()
    self.createActions()
    self.createMenu()
    self.show()

  def setUpWindow(self):
    pass

  def createActions(self):
    self.quit_act = QAction("&Quitter")
    self.quit_act.setShortcut("Ctrl+Q")
    self.quit_act.triggered.connect(self.close)

  def createMenu(self):
    file_menu = self.menuBar().addMenu("Fichier")
    file_menu.addAction(self.quit_act)

    edit_menu = self.menuBar().addMenu("Edition")

    exec_menu = self.menuBar().addMenu("Exécution")

    help_menu = self.menuBar().addMenu("Aide")

  def resizeEvent(self, event):
    pass
    
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec())