from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

def duplicate_widget(initial_widget):

  duplicated_widget = QWidget()

  duplicated_widget.setGeometry(initial_widget.geometry())
  duplicated_widget.setStyleSheet(initial_widget.styleSheet())

  initial_layout = initial_widget.layout()
  if initial_layout :
    duplicated_layout = duplicate_layout(initial_layout)
    duplicated_widget.setLayout(duplicated_layout)

  return duplicated_widget

def duplicate_layout(initial_layout):

  layout_type = type(initial_layout)
  new_layout = layout_type()

  new_layout.setSpacing(initial_layout.spacing())
  new_layout.setContentsMargins(initial_layout.contentsMargins())

  duplicate_box_layout(initial_layout, new_layout)

  return new_layout

def duplicate_box_layout(initial_layout, new_layout):

  for i in range(initial_layout.count()):
    item = initial_layout.itemAt(i)

    if item.widget():
      duplicated_inner_widget = duplicate_single_widget(item.widget())
      new_layout.addWidget(duplicated_inner_widget)

def duplicate_single_widget(original_widget):
  widget_type = type(original_widget)
  duplicated_widget = widget_type()
  copy_widget_properties(original_widget, duplicated_widget)
  
  return duplicated_widget

def copy_widget_properties(original, duplicated):

  # Propriétés de base
  duplicated.setGeometry(original.geometry())
  duplicated.setStyleSheet(original.styleSheet())
  duplicated.setFont(original.font())
  duplicated.setEnabled(original.isEnabled())
  duplicated.setVisible(original.isVisible())
  duplicated.setToolTip(original.toolTip())
  duplicated.setCursor(original.cursor())
  
  # Propriétés spécifiques selon le type
  if hasattr(original, 'text') and hasattr(duplicated, 'setText'):
    duplicated.setText(original.text())
  
  if hasattr(original, 'isChecked') and hasattr(duplicated, 'setChecked'):
    duplicated.setChecked(original.isChecked())
  
  if hasattr(original, 'value') and hasattr(duplicated, 'setValue'):
    duplicated.setValue(original.value())

  if original.metaObject().className() == "QComboBox" and hasattr(duplicated, "addItems"):
    items = [original.itemText(i) for i in range(original.count())]
    duplicated.addItems(items)
    duplicated.currentIndexChanged.connect(original._change_slot)

  if isinstance(original, QPushButton):
    if hasattr(original, "_clicked_slot"):
      duplicated.clicked.connect(original._clicked_slot)