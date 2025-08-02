from modules.engine.Color import Color
import curses

class Buffer : 
  def __init__(self,width,height):
    self.__width = width
    self.__height = height

    self.clear_data()

  def clear_data(self):
    columns = []
    for i in range(self.get_height()):
      rows = []
      for j in range(self.get_width()):
        rows.append([' ',Color(255,255,255),100])
      columns.append(rows)

    self.__data = columns

  def get_width(self):
    return self.__width
  def get_height(self):
    return self.__height
  def get_pixel(self,x,y):
    return self.__data[y][x]
  def get_data(self):
     return self.__data

  def set_width(self, n_width):
    self.__width = n_width
  def set_height(self, n_height):
    self.__height = n_height
  def set_pixel(self,x,y,n_content):
    self.__data[y][x] = n_content
  def set_data(self, n_data):
    self.__data = n_data

  def set_str_buffer(self,char,color,depth,x,y):
    if x+len(char) < self.get_width()+1 :
      if y < self.get_height() :
        if len(char) > 1 :
          x_acc = x
          for i in range(len(char)) :
            if self.get_pixel(x_acc,y)[2] >= depth :
              self.set_pixel(x_acc,y,[char[i],color,depth])
            x_acc += 1
        else :
          if self.get_pixel(x,y)[2] >= depth :
            self.set_pixel(x,y,[char,color,depth])

  def show_data(self, stdscr):
    for y, row in enumerate(self.get_data()):
      for x, cell in enumerate(row):
        char = cell[0]
        color = cell[1]
        # Utiliser une couleur de base (par exemple, blanc sur noir)
        try:
          stdscr.addstr(y, x, char, curses.color_pair(0))
        except curses.error:
          pass
    stdscr.refresh()
