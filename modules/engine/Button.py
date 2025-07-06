from modules.engine.Buffer import Buffer
from modules.engine.Image import Image

class Button : 
  def __init__(self,content,position,color1,color2):
    self.__content = content
    self.__position = position
    self.__color1 = color1
    self.__color2 = color2

  def get_content(self) :
    return self.__content
  def get_position(self):
    return self.__position
  def get_color1(self):
    return self.__color1
  def get_color2(self):
    return self.__color2

  def set_content(self, n_content):
    self.__content = n_content
  def set_position(self, n_position):
    self.__position = n_position
  def set_color1(self, n_color1):
    self.__color1 = n_color1
  def set_color2(self, n_color2):
    self.__color2 = n_color2

  def draw_text_button(self, window_inp, hover):
    if hover :
      color_drawing = self.get_color2()
    else :
      color_drawing = self.get_color1()
    space_needed = len(self.get_content())
    x_fix = self.get_position()[0]
    y_fix = self.get_position()[1]
    x_index = x_fix+1
    Buffer.set_str_buffer(window_inp,self.get_content(), color_drawing,0, x_fix+1,y_fix+2)
    Buffer.set_str_buffer(window_inp,'┌', color_drawing,0, x_fix,y_fix)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_fix,y_fix+1)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_fix,y_fix+2)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_fix,y_fix+3)
    Buffer.set_str_buffer(window_inp,'└', color_drawing,0, x_fix,y_fix+4)
    for i in range(space_needed):
      Buffer.set_str_buffer(window_inp,'─', color_drawing,0, x_index,y_fix)
      Buffer.set_str_buffer(window_inp,'─', color_drawing,0, x_index,y_fix+4)
      x_index += 1
    Buffer.set_str_buffer(window_inp,'┐', color_drawing,0, x_index,y_fix)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_index,y_fix+1)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_index,y_fix+2)
    Buffer.set_str_buffer(window_inp,'│', color_drawing,0, x_index,y_fix+3)
    Buffer.set_str_buffer(window_inp,'┘', color_drawing,0, x_index,y_fix+4)

  def draw_image_button(self, window_inp, hover):
    if hover :
      color_drawing = self.get_color2()
    else :
      color_drawing = self.get_color1()
    x_space_needed = len(Image.get_visual(self.get_content()[0])[0])+1
    y_space_needed = len(Image.get_visual(self.get_content()[0]))+1
    x_fix = self.get_position()[0]
    y_fix = self.get_position()[1]
    for color in self.get_content() :
      Image.set_pos(color,[x_fix+1,y_fix+1])
      Image.draw(color, window_inp)
    for y_index in range(y_fix+1,y_fix+y_space_needed):
      Buffer.set_str_buffer(window_inp,'|', color_drawing,0,x_fix,y_index)
      Buffer.set_str_buffer(window_inp,'|', color_drawing,0,x_fix+x_space_needed,y_index)
    for x_index in range(x_fix+1,x_fix+x_space_needed):
      Buffer.set_str_buffer(window_inp,'─', color_drawing,0,x_index,y_fix)
      Buffer.set_str_buffer(window_inp,'─', color_drawing,0,x_index,y_fix+y_space_needed)
    Buffer.set_str_buffer(window_inp,'┌', color_drawing,0,x_fix,y_fix)
    Buffer.set_str_buffer(window_inp,'└', color_drawing,0, x_fix,y_fix+y_space_needed)
    Buffer.set_str_buffer(window_inp,'┐', color_drawing,0, x_fix+x_space_needed,y_fix)
    Buffer.set_str_buffer(window_inp,'┘', color_drawing,0, x_fix+x_space_needed,y_fix+y_space_needed)