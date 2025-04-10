class NPC : pass

def create(x, y, name, visuals, pers_enigma):
  perso = NPC()
  
  perso.position = []
  perso.position.append(x)
  perso.position.append(y)

  perso.name = name
  perso.visuals = visuals
  perso.enigma = pers_enigma

  return perso

def get_position(perso_inp):
  return perso_inp.position
def get_name(perso_inp):
  return perso_inp.name
def get_visuals(perso_inp):
  return perso_inp.visuals
def get_enigma(perso_inp):
  return perso_inp.enigma

def set_position(perso_inp,n_x,n_y):
  perso_inp.position[0], perso_inp.position[1] = n_x, n_y
def set_name(perso_inp,n_name):
  perso_inp.name = n_name
def set_visuals(perso_inp, n_visuals):
  perso_inp.visuals = n_visuals
def set_enigma(perso_inp, n_enigma):
  perso_inp.enigma = n_enigma