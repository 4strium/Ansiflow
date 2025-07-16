import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtGui import QPainter, QPen, QColor, QPolygon, QBrush, QMouseEvent, QFont
from PyQt6.QtCore import Qt, QPoint
from modules.duplicateTools import duplicate_widget

class Bloc(QWidget) :
  def __init__(self, main_app, nb_inputs, nb_outputs, content, bloc_color, text_color, id=-1, unicity = False):
    super().__init__()
    self.mainApp = main_app
    self.nb_inputs = nb_inputs
    self.nb_outputs = nb_outputs
    self.content = content
    self.bloc_color = QColor(bloc_color)
    self.text_color = text_color
    self.id = id
    self.max_width = 150
    self.width_value = max(self.max_width*self.nb_inputs, self.max_width*self.nb_outputs)
    self.max_height = 100
    self.content_padding = 20
    self.content_size = 20
    self.visible = True
    self.unique = unicity
    self.new_pos = None
    self.already_moved = False
    self.dragging = False
    self.dragging_position = QPoint()

    self.initializeUI()

  def initializeUI(self):
    self.setCursor(Qt.CursorShape.OpenHandCursor)

    self.content.setParent(self)
    self.content.setStyleSheet(f"color: {self.text_color}; background: transparent;")
    self.content.move(self.content_padding, (self.max_height - self.content_size)//2)
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
          self.parent_pos = parent_widget.mapFromGlobal(central_widget.mapToGlobal(self.new_pos))
          self.move(self.parent_pos)
        else:
          self.move(self.new_pos)
      event.accept()
  
  def mouseReleaseEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragging = False
      self.setCursor(Qt.CursorShape.OpenHandCursor)
      event.accept()
      if self.mainApp.bloc_zone and self.new_pos :
        if (self.mainApp.bloc_zone[0][0] <= self.new_pos.x() <= self.mainApp.bloc_zone[1][0]) and (self.mainApp.bloc_zone[0][1] <= self.new_pos.y() <= self.mainApp.bloc_zone[1][1]) :
          if not self.already_moved :
            copy_content = duplicate_widget(self.content)
            bloc_copy = Bloc(self.mainApp, self.nb_inputs, self.nb_outputs, copy_content, self.bloc_color, self.text_color, self.id, self.unique)
            bloc_copy.setParent(self.mainApp.bloc_working_zone)
            bloc_copy.already_moved = True
            
            bloc_copy.content.adjustSize()
            bloc_copy.width_value = max(bloc_copy.max_width*bloc_copy.nb_inputs, bloc_copy.max_width*bloc_copy.nb_outputs)
            bloc_copy.setFixedSize(max(bloc_copy.width_value, bloc_copy.content.width()+(2*bloc_copy.content_padding)), bloc_copy.max_height + 40)
            
            bloc_copy.move(self.new_pos)
            bloc_copy.show()
            bloc_copy.raise_()
            if self.unique :
              self.hide()
            else : 
              self.move(self.pos_before_drag)
          else :
            self.move(self.parent_pos)
        else :
          if self.already_moved :
            if self.unique :
              for i in range(self.mainApp.pers_dialogue_layout.count()):
                widget = self.mainApp.pers_dialogue_layout.itemAt(i).widget()
                if widget is not None :   
                  if widget.id == self.id :
                    widget.show()
                    break
            self.setParent(None)
            self.deleteLater()
          else :
            self.move(self.pos_before_drag)
        self.mainApp.update()

  def hide(self):
    print(f"Bloc caché : {self} (id={self.id}, unique={self.unique})")
    super().hide()

  def show(self):
    print(f"Bloc montré : {self} (id={self.id}, unique={self.unique})")
    super().show()

