class Wall : pass

def create(color, texture="#", start_ind=0, width=0):
  wall_export = Wall()
  wall_export.texture = texture
  wall_export.start_ind = start_ind
  wall_export.end_ind = round(start_ind + width) +1
  wall_export.color = color
  return wall_export
  
def get_texture(wall_inp):
  return wall_inp.texture
def get_start_ind(wall_inp):
  return wall_inp.start_ind
def get_end_ind(wall_inp):
  return wall_inp.end_ind
def get_color(wall_inp):
  return wall_inp.color

def set_texture(wall_inp, n_texture):
  wall_inp.texture = n_texture
def set_start_ind(wall_inp, n_start_ind):
  wall_inp.start_ind = n_start_ind
def set_end_ind(wall_inp, n_end_ind):
  wall_inp.end_ind = n_end_ind
def set_color(wall_inp, n_color):
  wall_inp.color = n_color