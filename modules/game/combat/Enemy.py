import math
import json
import modules.game.Character as Character
from modules.game.Player import *
from modules.game.combat.Fight import *
from modules.engine.Buffer import Buffer
from modules.engine.Image import Image
from modules.engine.Color import Color

INCREMENT_RAD = 0.017

class Enemy(Character.Character):

  def __init__(self, visuals, x, y):
    super().__init__(x, y)
    self.__visuals = visuals
    self.__pv = 100

  def get_visuals(self): 
    return self.__visuals
  def set_visuals(self,visuals):
    self.__visuals = visuals
  def get_pv(self):
    return self.__pv
  def set_pv(self,pv):
    self.__pv = pv
  
  
  def shoot_enemy(self, window_inp, fight_game):
    center_x = window_inp.get_width() // 2
    center_y = window_inp.get_height() // 2
    if (window_inp.get_pixel(center_x + 2, center_y - 2)[0] not in [' ', '█']) or (window_inp.get_pixel(center_x + 3, center_y - 2)[0] not in [' ', '█']):
      self.set_pv(self.get_pv() - 10)
      if self.get_pv() <= 0:
        fight_game.get_enemy_list().remove(self)
        fight_game.set_flame_state(0)

  def upload_enemy(fight_inp, enemy_pack):

    try :
      with open(enemy_pack['path_visual'], 'r', encoding='utf-8') as file_txt:
        tmp = file_txt.readlines()
        content = [line.rstrip('\n') for line in tmp]
    except FileNotFoundError :
      return

    visuals = []
    for line in range(len(content)-1) :
      if "__VISUAL" in content[line] :
        nb_colors = int(content[line+1].split("__NBCOLORS__")[1].strip())
        line += 2
        colors = []
        for i in range(nb_colors) :
          red = int(content[line].split("__COLORR__")[1].strip())
          green = int(content[line+1].split("__COLORG__")[1].strip())
          blue = int(content[line+2].split("__COLORB__")[1].strip())
          line += 3

          tmp_visual = []
          while "__ENDVISUAL__" not in content[line] :
            tmp_visual.append(content[line])
            line += 1
          line += 1
          colors.append(Image(tmp_visual,0,0,Color(red,green,blue)))
        visuals.append(colors)

    fight_inp.get_enemy_list().append(Enemy(visuals,enemy_pack['position'][0],enemy_pack['position'][1]))

  def dispatch_Enemies(fight_inp, data_path):
    with open(data_path, 'r') as file :
      data = json.load(file)
    enemy_elements = data['Enemy']

    for ene in enemy_elements :
      Enemy.upload_enemy(fight_inp, ene)

  def draw_Enemy(window_inp, fight_inp, player_inp, UI_color):
    for enemy_t in fight_inp.get_enemy_list() :
      distance = math.sqrt((enemy_t.get_position()[0] - player_inp.get_position()[0])**2 + (enemy_t.get_position()[1] - player_inp.get_position()[1])**2)

      if 0.01 < distance < 2.0 :
        vector_origin = (math.cos(player_inp.get_angle()),math.sin(player_inp.get_angle()))
        vector_NPC = (enemy_t.get_position()[0] - player_inp.get_position()[0], enemy_t.get_position()[1] - player_inp.get_position()[1])
        angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

        fov_limits = (player_inp.get_fov()//2)*INCREMENT_RAD
        x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * window_inp.get_width())

        if -fov_limits <= angle_player_npc <= fov_limits :
          for i in range(len(enemy_t.get_visuals()[0])):
            Image.set_pos(enemy_t.get_visuals()[0][i],[x_fix,2])
            Image.draw(enemy_t.get_visuals()[0][i],window_inp, distance)
      # Écrire les PV via le buffer interne
      Buffer.set_str_buffer(window_inp, str(enemy_t.get_pv())+" PV", UI_color,0,window_inp.get_width()//2, 0)
