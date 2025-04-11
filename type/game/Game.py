import curses
import math
import type.game.Player as Player
import type.game.NPC as NPC
import type.game.Image as Image
import type.game.Player_Window as P_win

INCREMENT_RAD = 0.017
PI = 3.142

class Game : pass

def create(differential_time, map, npc_list=[]):
  game_export = Game()
  game_export.time = 0
  game_export.dt = differential_time
  game_export.map = map
  game_export.npc_list = npc_list
  return game_export

def get_time(game_inp):
  return game_inp.time
def get_diff_time(game_inp):
  return game_inp.dt
def get_map(game_inp):
  return game_inp.map
def get_npcs(game_inp):
  return game_inp.npc_list

def set_diff_time(game_inp, n_dt):
  game_inp.dt = n_dt
def set_map(game_inp,n_map):
  game_inp.map = n_map
def set_npcs(game_inp,n_npcs):
  game_inp.npcs = n_npcs

def running_time(game_inp):
  game_inp.time += get_diff_time(game_inp)

def draw_NPC(window_inp, game_inp, player_inp):
  for npc_g in game_inp.npc_list :
    distance = math.sqrt((NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0])**2+(NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])**2)

    if distance < 10 :
      P_win.get_stdscr(window_inp).addstr(0, P_win.get_width(window_inp) // 2, str(round(distance,3)), 1)
      P_win.get_stdscr(window_inp).addstr(1, P_win.get_width(window_inp) // 2, str(game_inp.npc_list[0].name), 1)

    if 0.01 < distance < 2.5 :
      if distance > 1.65 :
        dist_version = 0
      elif distance > 0.825 :
        dist_version = 1
      else :
        dist_version = 2
      vector_origin = (math.cos(Player.get_angle(player_inp)),math.sin(Player.get_angle(player_inp)))
      vector_NPC = (NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0], NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])
      angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

      fov_limits = (Player.get_fov(player_inp)//2)*INCREMENT_RAD
      x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * P_win.get_width(window_inp))

      if -fov_limits <= angle_player_npc <= fov_limits :
        Image.set_pos(npc_g.visuals[dist_version],[x_fix,(P_win.get_height(window_inp) // 5)*2])
        Image.draw(window_inp, NPC.get_visuals(npc_g)[dist_version])
      P_win.get_stdscr(window_inp).addstr(2, P_win.get_width(window_inp) // 2, str(angle_player_npc), 1)
