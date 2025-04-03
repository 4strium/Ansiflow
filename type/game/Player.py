import math
import type.game.Player_Window as P_win

class Player : pass

def create(position, fov):
  player_export = Player()
  player_export.position = position
  player_export.fov = fov
  player_export.angle = 0.
  return player_export

def get_position(player_inp) : return player_inp.position
def get_fov(player_inp) : return player_inp.fov
def get_angle(player_inp) : return player_inp.angle

def set_position(player_inp, n_pos): player_inp.position = n_pos
def set_fov(player_inp, n_fov) : player_inp.fov = n_fov
def set_angle(player_inp, n_angle) : player_inp.angle = n_angle

def move(player, dt, window):
  key = P_win.get_stdscr(window).getch()

  if key == 27:  # Quitter avec 'échap'
    exit()
  elif key == ord('z'):
    # Simuler l'avancement du personnage :
    player.position[0] += dt * 5 * math.cos(get_angle(player))
    player.position[1] += dt * 5 * math.sin(get_angle(player))
    P_win.get_stdscr(window).clear()
  elif key == ord('s'):
    # Simuler le reculement du personnage par rapport au sol :
    player.position[0] -= dt * 5 * math.cos(get_angle(player))
    player.position[1] -= dt * 5 * math.sin(get_angle(player)) 
    P_win.get_stdscr(window).clear()  
  elif key == ord('q'):
    player.angle += dt * 5
    P_win.get_stdscr(window).clear()
  elif key == ord('d'):
    player.angle -= dt * 5
    P_win.get_stdscr(window).clear()