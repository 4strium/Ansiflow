class Color : 
  def __init__(self, R, G, B):
    self.__red = R
    self.__green = G
    self.__blue = B

  def get_red(self):
    return self.__red
  def get_green(self):
    return self.__green
  def get_blue(self):
    return self.__blue

  def set_red(self, n_red):
    self.__red = n_red
  def set_green(self, n_green):
    self.__green = n_green
  def set_blue(self, n_blue):
    self.__blue = n_blue