import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygon, QBrush, QMouseEvent, QFont
from PyQt6.QtCore import Qt, QPoint

class Bloc(QWidget) :
  def __init__(self, main_app, nb_inputs, nb_outputs, content, bloc_color, text_color, font, drag_zone = None):
    super().__init__()
    self.mainApp = main_app
    self.nb_inputs = nb_inputs
    self.nb_outputs = nb_outputs
    self.content = content
    self.bloc_color = QColor(bloc_color)
    self.text_color = text_color
    self.text_font = font
    self.max_width = 150
    self.width_value = max(self.max_width*self.nb_inputs, self.max_width*self.nb_outputs)
    self.max_height = 100
    self.content_padding = 20
    self.visible = True

    self.dragging = False
    self.dragging_position = QPoint()

    self.dragging_area = drag_zone

    self.initializeUI()

  def initializeUI(self):
    self.setCursor(Qt.CursorShape.OpenHandCursor)

    self.content.setParent(self)
    self.content.setFont(self.text_font)
    self.content.setStyleSheet(f"color: {self.text_color}; background: transparent;")
    self.content.move(self.content_padding, (self.max_height - self.text_font.pointSize())//2)
    self.content.raise_()

  def setNbInputs(self, nb_inp):
    self.nb_inputs = nb_inp
  
  def setNbOutputs(self, nb_out):
    self.nb_outputs = nb_out
  
  def setVisibility(self, visi):
    self.visible = visi
  
  def paintEvent(self, event):
    if not self.visible :
      return
    
    painter = QPainter(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setPen(QPen(self.bloc_color, 1))
    painter.setBrush(QBrush(self.bloc_color))
    
    polygon = [
      QPoint(0,0),
      QPoint(max(self.width_value, self.content.width()+(2*self.content_padding)),0),
      QPoint(max(self.width_value, self.content.width()+(2*self.content_padding)), self.max_height),
      QPoint(0, self.max_height)
    ]

    for i in range(self.nb_inputs):
      polygon.insert((i*3)+1,QPoint(self.max_width*i+5,0))
      polygon.insert((i*3)+2,QPoint(self.max_width*i+15,20))
      polygon.insert((i*3)+3,QPoint(self.max_width*i+25,0))


    for j in range(self.nb_outputs,0,-1):
      idx = len(polygon) - 1
      polygon.insert(idx, QPoint(self.max_width*(j-1)+25, self.max_height))
      polygon.insert(idx+1, QPoint(self.max_width*(j-1)+15, self.max_height+20))
      polygon.insert(idx+2, QPoint(self.max_width*(j-1)+5, self.max_height))

    painter.drawPolygon(QPolygon(polygon))


  def mousePressEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragging = True
      self.setCursor(Qt.CursorShape.ClosedHandCursor)
      self.pos_before_drag = self.pos()
      self.drag_position = event.position().toPoint()
      event.accept()

  def mouseMoveEvent(self, event: QMouseEvent):
    if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
      # Position globale de la souris
      global_mouse_pos = event.globalPosition().toPoint()
      
      # Convertir en position locale dans le widget central
      central_widget = self.mainApp.centralWidget()
      if central_widget:
        local_mouse_pos = central_widget.mapFromGlobal(global_mouse_pos)
        # Nouvelle position du bloc relative au widget central
        self.new_pos = local_mouse_pos - self.drag_position
        
        # Convertir en position locale pour le parent direct
        parent_widget = self.parent()
        if parent_widget and central_widget != parent_widget:
          parent_pos = parent_widget.mapFromGlobal(central_widget.mapToGlobal(self.new_pos))
          self.move(parent_pos)
        else:
          self.move(self.new_pos)
          
      event.accept()
  
  def mouseReleaseEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragging = False
      self.setCursor(Qt.CursorShape.OpenHandCursor)
      event.accept()
      if self.dragging_area :
        if (self.dragging_area[0][0] <= self.new_pos.x() <= self.dragging_area[1][0]) and (self.dragging_area[0][1] <= self.new_pos.y() <= self.dragging_area[1][1]) :
          pass
        else :
          self.move(self.pos_before_drag)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bloc PyQt6")
        main_layout = QVBoxLayout()

        bloc_btn_stylesheet = """
          QPushButton {
            background-color : white;
            color : black;
            border-radius : 10px;
            padding : 10px;
            padding-top: 4px;
            padding-bottom : 4px;
          }
          QPushButton:hover{
            background-color: #c9c9c9;
          }
        """

        bloc_combobox_stylesheet = """
          QComboBox {
            background-color : white;
            color : black;
            border-radius : 10px;
            padding : 10px;
            padding-top: 4px;
            padding-bottom : 4px;
          }
          QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            selection-background-color: #c9c9c9;
            selection-color: black;
            padding: 4px;
          }
        """

        print_text_layout = QHBoxLayout()
        print_text_layout.setContentsMargins(0,0,0,0)
        afficher = QLabel("Afficher")
        texte_btn = QPushButton("texte")
        texte_btn.setFont(QFont("Arial", 20))
        texte_btn.setStyleSheet(bloc_btn_stylesheet)
        print_text_layout.addWidget(afficher)
        print_text_layout.addWidget(texte_btn)
        print_text = QWidget()
        print_text.setLayout(print_text_layout)
        main_layout.addWidget(Bloc(1,1, print_text, "#00ccff", "#FFFFFF", QFont("Arial", 20)))

        ask_layout = QHBoxLayout()
        ask_layout.setContentsMargins(0,0,0,0)
        poser = QLabel("Poser")
        ask_btn = QPushButton("question")
        ask_btn.setFont(QFont("Arial", 20))
        ask_btn.setStyleSheet(bloc_btn_stylesheet)
        a_text = QLabel("à")
        nb_answers_selector = QComboBox()
        nb_answers_selector.setFont(QFont("Arial", 20))
        nb_answers_selector.setStyleSheet(bloc_combobox_stylesheet)
        nb_answers_selector.addItems(["2","3"])
        answers_text = QLabel("réponses")
        ask_layout.addWidget(poser)
        ask_layout.addWidget(ask_btn)
        ask_layout.addWidget(a_text)
        ask_layout.addWidget(nb_answers_selector)
        ask_layout.addWidget(answers_text)
        ask_container = QWidget()
        ask_container.setLayout(ask_layout)
        main_layout.addWidget(Bloc(1,3,ask_container, "#ff00b3", "#FFFFFF", QFont("Arial", 20)))


        main_layout.addWidget(Bloc(0,1,QLabel("DÉBUT"), "#15ff00", "#FFFFFF", QFont("Arial", 20)))
        main_layout.addWidget(Bloc(1,0,QLabel("FIN"), "#ffae00", "#FFFFFF", QFont("Arial", 20)))
        main_layout_container = QWidget()
        main_layout_container.setLayout(main_layout)
        self.setCentralWidget(main_layout_container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

