class Card :
  def __init__(self,id,visual,couple_id):
    self.__id = id
    self.__visual = visual
    self.__couple_id = couple_id 

  def get_id(self): 
    return self.__id
  def set_id(self, n_id): 
    self.__id = n_id
  def get_visual(self): 
    return self.__visual
  def set_visual(self, n_visual): 
    self.__visual = n_visual
  def get_couple_id(self): 
    return self.__couple_id
  def set_couple_id(self, n_couple): 
    self.__couple_id = n_couple
