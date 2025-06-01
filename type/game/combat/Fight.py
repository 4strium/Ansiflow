import math
import engine.Image as Image
import engine.Buffer as Buffer
from type.game.Player import Player
from type.game.combat.Enemy import Enemy

class Fight : 
  def __init__(self,window_inp):
    self.__target_image = Image.upload_with_colors("images/target.txt")[0] # Possible car couleur unique
    Image.set_pos(self.__target_image,[(Buffer.get_width(window_inp)//2)-7,(Buffer.get_height(window_inp)//2)-7])

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

  def update_fight(self, window_inp, UI_color):
    Image.draw(window_inp, self.get_target_image())
    for color in self.get_weapon_image() :
      Image.set_pos(color,[Buffer.get_width(window_inp)-60,Buffer.get_height(window_inp)-25])
      Image.draw(window_inp,color)
    if self.get_flame_state() > 0 :
      for color2 in self.get_flame_image() :
        Image.set_pos(color2,[Buffer.get_width(window_inp)-74,Buffer.get_height(window_inp)-33])
        Image.draw(window_inp,color2)
      current_state = self.get_flame_state()
      self.set_flame_state(current_state - 1)
    Buffer.set_str_buffer(window_inp,"Appuie sur ESPACE pour lui tirer dessus !",UI_color,0, (Buffer.get_width(window_inp)//3)+14,Buffer.get_height(window_inp)-8)