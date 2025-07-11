import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygon, QBrush, QMouseEvent
from PyQt6.QtCore import Qt, QPoint

class Bloc(QWidget) :
  def __init__(self, nb_inputs, nb_outputs, content, bloc_color, text_color):
    super().__init__()
    self.nb_inputs = nb_inputs
    self.nb_outputs = nb_outputs
    self.content = content
    self.bloc_color = QColor(bloc_color)
    self.text_color = QColor(text_color)
    self.max_width = 150
    self.width_value = max(self.max_width*self.nb_inputs, self.max_width*self.nb_outputs)
    self.max_height = 100
    self.visible = True

    self.dragging = False
    self.dragging_position = QPoint()

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
      QPoint(self.width_value,0),
      QPoint(self.width_value, self.max_height),
      QPoint(0, self.max_height)
    ]

    for i in range(self.nb_inputs):
      polygon.insert((i*3)+1,QPoint(self.max_width*i+10,0))
      polygon.insert((i*3)+2,QPoint(self.max_width*i+15,20))
      polygon.insert((i*3)+3,QPoint(self.max_width*i+20,0))


    for j in range(self.nb_outputs,0,-1):
      idx = len(polygon) - 1
      polygon.insert(idx, QPoint(self.max_width*(j-1)+20, self.max_height))
      polygon.insert(idx+1, QPoint(self.max_width*(j-1)+15, self.max_height+20))
      polygon.insert(idx+2, QPoint(self.max_width*(j-1)+10, self.max_height))

    painter.drawPolygon(QPolygon(polygon))
    painter.setPen(QPen(self.text_color))
    painter.drawText(20,self.max_height//2,self.content)

  def mousePressEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragging = True
      self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
      event.accept()
    
  def mouseMoveEvent(self, event: QMouseEvent):
    if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
      new_pos = event.globalPosition().toPoint() - self.drag_position
      self.move(new_pos)
      event.accept()
  
  def mouseReleaseEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragging = False
      event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bloc PyQt6")
        main_layout = QVBoxLayout()
        main_layout.addWidget(Bloc(3,3,"TEST", "#00ccff", "#FFFFFF"))
        main_layout.addWidget(Bloc(1,3,"TEST 2", "#ff00b3", "#FFFFFF"))
        main_layout.addWidget(Bloc(2,2,"TEST 3", "#15ff00", "#FFFFFF"))
        main_layout_container = QWidget()
        main_layout_container.setLayout(main_layout)
        self.setCentralWidget(main_layout_container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
  
    