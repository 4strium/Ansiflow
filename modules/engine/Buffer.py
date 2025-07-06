from modules.engine.Color import Color

class Buffer() : 
  def __init__(self, emu_terminal):

    self.clear_data(emu_terminal)

  def clear_data(self, terminal):
    columns = []
    for i in range(terminal.getHeight()):
      rows = []
      for j in range(terminal.getWidth()):
        rows.append([' ',Color(255,255,255),100])
      columns.append(rows)

    self.__data = columns

  def get_pixel(self,x,y):
    return self.__data[y][x]
  def get_data(self):
    return self.__data
  def set_pixel(self,x,y,n_content):
    self.__data[y][x] = n_content
  def set_data(self, n_data):
    self.__data = n_data

  def set_str_buffer(terminal,char,color,depth,x,y):
    if x+len(char) < terminal.getWidth()+1 :
      if len(char) > 1 :
        x_acc = x
        for i in range(len(char)) :
          if terminal.buffer.get_pixel(x_acc,y)[2] >= depth :
            terminal.buffer.set_pixel(x_acc,y,[char[i],color,depth])
          x_acc += 1
      else :
        if terminal.buffer.get_pixel(x,y)[2] >= depth :
          terminal.buffer.set_pixel(x,y,[char,color,depth])