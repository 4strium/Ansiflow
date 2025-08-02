from modules.engine.Buffer import Buffer
from modules.engine.Color import Color

class Image : 
  def __init__(self, visual, x, y, color):
    self.__visual = visual
    self.__position = [x,y]
    self.__color = color    

  def get_visual(self):
    return self.__visual
  def get_pos(self):
    return self.__position
  def get_color(self):
    return self.__color

  def set_visual(self, n_visu):
    self.__visual = n_visu
  def set_pos(self, n_pos):
    self.__position = n_pos
  def set_color(self, n_color):
    self.__color = n_color

  def upload_classic_image(path, x, y, color) :
    try :
      with open(path, 'r', encoding='utf-8') as file_txt:
        tmp = file_txt.readlines()
        visual_export = [line.rstrip('\n') for line in tmp]
    except FileNotFoundError :
      return
    
    return Image(visual_export, x, y, color)

  def upload_with_colors(path):
    try :
      with open(path, 'r', encoding='utf-8') as file_txt:
        tmp = file_txt.readlines()
        content = [line.rstrip('\n') for line in tmp]
    except FileNotFoundError :
      return
    

    nb_colors = int(content[0].split("__NBCOLORS__")[1].strip())
    colors = []
    line = 1

    for i in range(nb_colors) :
      red = int(content[line].split("__COLORR__")[1].strip())
      green = int(content[line+1].split("__COLORG__")[1].strip())
      blue = int(content[line+2].split("__COLORB__")[1].strip())
      line += 3

      tmp_visual = []
      while "__ENDCONTENT__" not in content[line] :
        tmp_visual.append(content[line])
        line += 1
      line += 1
      colors.append(Image(tmp_visual,0,0,Color(red,green,blue)))

    return colors

  def draw(self, window, depth = 0):
    height = window.get_height()
    width = window.get_width()

    for i in range(len(self.get_visual())):
      y_pos = i + self.get_pos()[1]
      if 0 <= y_pos < height:  # Ensure y_pos is within window bounds
        x_offset = 0
        # On affiche caractère par caractère car on veut pouvoir "détourer les images"
        for char in self.get_visual()[i]:
          x_pos = self.get_pos()[0] + x_offset
          if char != '1' and 0 <= x_pos < width-1:  # Ensure x_pos is within bounds
            Buffer.set_str_buffer(window, char, self.get_color(), depth, x_pos, y_pos)
          x_offset += 1