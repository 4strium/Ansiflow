import math
from modules.engine.Image import Image
from modules.engine.Buffer import Buffer
from modules.game.Player import Player

class Fight : 
  def __init__(self,terminal):
    self.__target_image = Image.upload_with_colors("images/target.txt")[0] # Possible car couleur unique
    Image.set_pos(self.__target_image,[(terminal.getWidth()//2)-7,(terminal.getHeight()//2)-7])

    self.__weapon_image = Image.upload_with_colors("images/weapon-1.txt")
    self.__flame_image = Image.upload_with_colors("images/flamme.txt")
    self.__flame_state = 0
    self.__enemy_list = []

  def get_target_image(self):
    return self.__target_image
  def set_target_image(self,target_image):
    self.__target_image = target_image
  def get_weapon_image(self):
    return self.__weapon_image
  def set_weapon_image(self,weapon_image):
    self.__weapon_image = weapon_image
  def get_flame_image(self):
    return self.__flame_image
  def set_flame_image(self,flame_image):
    self.__flame_image = flame_image
  def get_flame_state(self):
    return self.__flame_state
  def set_flame_state(self,flame_state):
    self.__flame_state = flame_state
  def get_enemy_list(self):
    return self.__enemy_list
  def set_enemy_list(self,enemy_list):
    self.__enemy_list = enemy_list

  def is_fight_time(self, player_inp):
    for enemy_t in self.get_enemy_list():
      distance = math.sqrt((enemy_t.get_position()[0] - Player.get_position(player_inp)[0])**2 + (enemy_t.get_position()[1] - Player.get_position(player_inp)[1])**2)

      if 0.01 < distance < 2.5 :
        return [True,enemy_t]
    
    return[False,None]

  def update_fight(self, terminal_inp, UI_color):
    Image.draw(self.get_target_image(),terminal_inp)
    for color in self.get_weapon_image() :
      Image.set_pos(color,[terminal_inp.getWidth()-60,terminal_inp.getHeight()-25])
      Image.draw(color,terminal_inp)
    if self.get_flame_state() > 0 :
      for color2 in self.get_flame_image() :
        Image.set_pos(color2,[terminal_inp.getWidth()-74,terminal_inp.getHeight()-33])
        Image.draw(color2,terminal_inp)
      current_state = self.get_flame_state()
      self.set_flame_state(current_state - 1)
    Buffer.set_str_buffer(terminal_inp.buffer,"Appuie sur ESPACE pour lui tirer dessus !",UI_color,0, (terminal_inp.getWidth()//3)+14,terminal_inp.getHeight()-8)