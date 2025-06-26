class Character :
  def __init__(self,x,y):
    self.__position=[x,y]

  def get_position(self):
    return self.__position
  
  def set_position(self,x,y):
    self.__position =[x,y]