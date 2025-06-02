import sys
from engine.Color import Color

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
      if len(char) > 1 :
        x_acc = x
        for i in range(len(char)) :
          if self.get_pixel(x_acc,y)[2] >= depth :
            self.set_pixel(x_acc,y,[char[i],color,depth])
          x_acc += 1
      else :
        if self.get_pixel(x,y)[2] >= depth :
          self.set_pixel(x,y,[char,color,depth])


  def rgb_fg(r, g, b):
      return f"\033[38;2;{r};{g};{b}m"

  def move_to(x, y):
      return f"\033[{y};{x}H"

  def reset():
      return "\033[0m"

  def show_data(self):
      output = []
      prev_fg = None

      for y, row in enumerate(self.get_data(), start=1):
          output.append(Buffer.move_to(1, y))
          for cell in row:
              char = cell[0]
              color_fg = [Color.get_red(cell[1]),Color.get_green(cell[1]),Color.get_blue(cell[1])]

              # Moduler la couleur en fonction de la profondeur
              if cell[2] > 2:
                depth_factor = (1 - (max(2, min(6, cell[2])) / 8))*1.1
                color_fg = [
                int(color_fg[0] * depth_factor),
                int(color_fg[1] * depth_factor),
                int(color_fg[2] * depth_factor),
                ]

              # Changer couleur si nécessaire
              if color_fg != prev_fg:
                  if color_fg :
                      output.append(Buffer.rgb_fg(color_fg[0],color_fg[1],color_fg[2]))
                  else:
                      output.append("\033[39m")  # couleur par défaut
                  prev_fg = color_fg

              output.append("\033[49m")  # fond par défaut

              output.append(char)

      output.append(Buffer.reset())
      sys.stdout.write("".join(output))
      sys.stdout.flush()