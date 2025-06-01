class Wall : 
  def __init__(self,color,texture="#",start_ind=0,width=0):
    self.__color = color
    self.__texture=texture
    self.__start_ind = start_ind
    self.__end_ind = int(start_ind + width) + 1
    self.__width = width

  def get_color(self):
    return self.__color
  def set_color(self,color):
    self.__color = color
  def get_texture(self):
    return self.__texture
  def set_texture(self,texture):
    self.__texture = texture
  def get_start_ind(self):
    return self.__start_ind
  def set_start_ind(self,start_ind):
    self.__start_ind = start_ind
  def get_end_ind(self):
    return self.__end_ind
  def set_end_ind(self,end_ind):
    self.__end_ind = end_ind
  def get_width(self):
    return self.__width
  def set_width(self,width):
    self.__width = width