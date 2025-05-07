import math
import json
import type.game.Player as Player
import type.game.combat.Fight as Fight
import engine.Buffer as Buffer
import engine.Image as Image
import engine.Color as Color

INCREMENT_RAD = 0.017

class Enemy : pass

def create(visuals, x, y):
  enemy_element = Enemy()

  enemy_element.visuals = visuals
  enemy_element.position = [x,y]
  enemy_element.pv = 100
  enemy_element.power = 1

  return enemy_element

def get_position(enemy_inp): return enemy_inp.position
def get_visuals(enemy_inp): return enemy_inp.visuals
def get_pvs(enemy_inp): return enemy_inp.pv

def set_pvs(enemy_inp, n_pv):
  enemy_inp.pv = n_pv

def shoot_ennemy(window_inp, enemy_inp, fight_game):
  if (Buffer.get_pixel(window_inp,(Buffer.get_width(window_inp)//2)+2,(Buffer.get_height(window_inp)//2)-2)[0] not in [' ', '█']) or ( Buffer.get_pixel(window_inp,(Buffer.get_width(window_inp)//2)+3,(Buffer.get_height(window_inp)//2)-2)[0] not in [' ', '█']) :
    set_pvs(enemy_inp,get_pvs(enemy_inp)-10)

    if get_pvs(enemy_inp) <= 0 :
      Fight.get_enemy_list(fight_game).remove(enemy_inp)

def upload_enemy(figth_inp, enemy_pack):

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


        print(content[line])

        tmp_visual = []
        while "__ENDVISUAL__" not in content[line] :
          tmp_visual.append(content[line])
          line += 1
        line += 1
        colors.append(Image.create(tmp_visual,0,0,Color.create_color(red,green,blue)))
      visuals.append(colors)

  print(visuals)

  figth_inp.enemy_list.append(create(visuals,enemy_pack['position'][0],enemy_pack['position'][1]))

def dispatch_Enemies(fight_inp, data_path):
  with open(data_path, 'r') as file :
    data = json.load(file)
  enemy_elements = data['Enemy']

  for ene in enemy_elements :
    upload_enemy(fight_inp, ene)

def draw_Enemy(window_inp, fight_inp, player_inp, UI_color):
  for enemy_t in fight_inp.enemy_list :
    distance = math.sqrt((get_position(enemy_t)[0] - Player.get_position(player_inp)[0])**2 + (get_position(enemy_t)[1] - Player.get_position(player_inp)[1])**2)

    if 0.01 < distance < 2.5 :
      vector_origin = (math.cos(Player.get_angle(player_inp)),math.sin(Player.get_angle(player_inp)))
      vector_NPC = (get_position(enemy_t)[0] - Player.get_position(player_inp)[0], get_position(enemy_t)[1] - Player.get_position(player_inp)[1])
      angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

      fov_limits = (Player.get_fov(player_inp)//2)*INCREMENT_RAD
      x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * Buffer.get_width(window_inp))

      if -fov_limits <= angle_player_npc <= fov_limits :
        for i in range(len(get_visuals(enemy_t)[0])):
          Image.set_pos(enemy_t.visuals[0][i],[x_fix,2])
          Image.draw(window_inp, get_visuals(enemy_t)[0][i])
      Buffer.set_str_buffer(window_inp, str(angle_player_npc),UI_color,Buffer.get_width(window_inp) // 2, 2)
      Buffer.set_str_buffer(window_inp, str(enemy_t.pv)+" PV", UI_color,Buffer.get_width(window_inp)-6, 1)