import game.Character as Character

INCREMENT_RAD = 0.017

class Player(Character.Character):
  def __init__(self, x, y, fov, start_angle):
    super().__init__(x, y)
    self.__fov = fov
    self.__angle = start_angle
    self.__left_angle = self.__angle + (self.__fov//2) * INCREMENT_RAD
  
  def get_fov(self):
    return self.__fov
  def set_fov(self,fov):
    self.__fov = fov
  def get_angle(self):
    return self.__angle
  def set_angle(self,angle):
    self.__angle = angle
    self.__left_angle = self.__angle + (self.__fov//2) * INCREMENT_RAD
  def get_left_angle(self):
    return self.__left_angle