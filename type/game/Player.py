import math
import sys
import termios
import engine.Buffer as Buffer
import type.game.Game as Game

INCREMENT_RAD = 0.017
PI = 3.142

class Player : pass

def create(position, fov):
  player_export = Player()
  player_export.position = position
  player_export.fov = fov
  player_export.angle = 0.
  player_export.left_angle = player_export.angle + (player_export.fov//2) * INCREMENT_RAD
  return player_export

def get_position(player_inp) : return player_inp.position
def get_fov(player_inp) : return player_inp.fov
def get_angle(player_inp) : return player_inp.angle
def get_left_angle(player_inp): return player_inp.left_angle

def set_position(player_inp, n_pos): player_inp.position = n_pos
def set_fov(player_inp, n_fov) : player_inp.fov = n_fov
def set_angle(player_inp, n_angle) : 
  player_inp.angle = n_angle
  player_inp.left_angle = player_inp.angle + (player_inp.fov//2) * INCREMENT_RAD

def move(game_inp,player, window, key):
  dt = Game.get_diff_time(game_inp)

  if key == ord('z'):
    # Simuler l'avancement du personnage :
    player.position[0] += dt * 5 * math.cos(get_angle(player))
    player.position[1] += dt * 5 * math.sin(get_angle(player))
    Buffer.clear_data(window)
  elif key == ord('s'):
    # Simuler le reculement du personnage par rapport au sol :
    player.position[0] -= dt * 5 * math.cos(get_angle(player))
    player.position[1] -= dt * 5 * math.sin(get_angle(player)) 
    Buffer.clear_data(window) 
  elif key == ord('q'):
    set_angle(player, player.angle + dt*5)
    Buffer.clear_data(window)
  elif key == ord('d'):
    set_angle(player, player.angle - dt*5)
    Buffer.clear_data(window)