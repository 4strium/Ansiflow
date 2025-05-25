import math
import engine.Image as Image
import engine.Buffer as Buffer
import type.game.Player as Player
import type.game.combat.Enemy as Enemy

class Fight : pass

def create(window_inp):
  fight_element = Fight()
  fight_element.target_image = Image.upload_with_colors("images/target.txt")[0] # Possible car couleur unique
  Image.set_pos(fight_element.target_image,[(Buffer.get_width(window_inp)//2)-7,(Buffer.get_height(window_inp)//2)-7])

  fight_element.weapon_image = Image.upload_with_colors("images/weapon-1.txt")
  fight_element.flame_image = Image.upload_with_colors("images/flamme.txt")
  fight_element.flame_state = 0

  fight_element.enemy_list = []

  return fight_element

def get_enemy_list(fight_inp): return fight_inp.enemy_list

def set_enemy_list(fight_game, n_enemy_list) :
  fight_game.enemy_list = n_enemy_list

def is_fight_time(fight_inp, player_inp):
  for enemy_t in get_enemy_list(fight_inp):
    distance = math.sqrt((Enemy.get_position(enemy_t)[0] - Player.get_position(player_inp)[0])**2 + (Enemy.get_position(enemy_t)[1] - Player.get_position(player_inp)[1])**2)

    if 0.01 < distance < 2.5 :
      return [True,enemy_t]
  
  return[False,None]

def update_fight(window_inp, fight_inp, UI_color):
  Image.draw(window_inp, fight_inp.target_image)
  for color in fight_inp.weapon_image :
    Image.set_pos(color,[Buffer.get_width(window_inp)-60,Buffer.get_height(window_inp)-25])
    Image.draw(window_inp,color)
  if fight_inp.flame_state > 0 :
    for color2 in fight_inp.flame_image :
      Image.set_pos(color2,[Buffer.get_width(window_inp)-74,Buffer.get_height(window_inp)-33])
      Image.draw(window_inp,color2)
    fight_inp.flame_state -= 1
  Buffer.set_str_buffer(window_inp,"Appuie sur ESPACE pour lui tirer dessus !",UI_color,0, (Buffer.get_width(window_inp)//3)+14,Buffer.get_height(window_inp)-8)