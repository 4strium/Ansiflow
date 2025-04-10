import curses
import math
import type.game.Player as Player
import type.game.NPC as NPC


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

def draw_NPC(game_inp, player_inp):
  for npc_g in game_inp.npc_list :
    if 0.01 < math.sqrt((NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0])**2+(NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])**2) < 10 :
      pass