import curses
import math
import time
import type.game.Player as Player
import type.game.NPC as NPC
import type.game.Image as Image
import type.game.Player_Window as P_win
import engine.Color as Color


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

def draw_backtalk(window_inp, color):
  for i in range(P_win.get_width(window_inp)):
    P_win.get_stdscr(window_inp).addstr((P_win.get_height(window_inp) // 3)*2, i, "─", color)
  for j in range((P_win.get_height(window_inp) // 3)*2+1,P_win.get_height(window_inp)-1):
    for k in range(P_win.get_width(window_inp)):
      P_win.get_stdscr(window_inp).addstr(j, k, " ", color)
