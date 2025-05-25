INCREMENT_RAD = 0.017

class Player : pass

def create(position, fov, start_angle):
  player_export = Player()
  player_export.position = position
  player_export.fov = fov
  player_export.angle = start_angle
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