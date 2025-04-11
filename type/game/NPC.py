import type.game.Image as Image
import engine.Color as Color

class NPC : pass

def create(x, y, name, visuals, pers_enigma=""):
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

def upload_NPC_to_game( game_inp, path):
  try :
    with open(path, 'r', encoding='utf-8') as file_txt:
      tmp = file_txt.readlines()
      content = [line.rstrip('\n') for line in tmp]
  except FileNotFoundError :
    return

  visuals = []
  for line in range(len(content)-1):
    if "__NAME__" in content[line]:
      name = content[line].split("__NAME__")[1].strip()
    elif "__POSITIONX__" in content[line]:
      posx = float(content[line].split("__POSITIONX__")[1].strip())
    elif "__POSITIONY__" in content[line]:
      posy = float(content[line].split("__POSITIONY__")[1].strip())
    elif "__VISUAL" in content[line]:
      nb_colors = int(content[line+1].split("__NBCOLORS__")[1].strip())
      red = int(content[line+2].split("__COLORR__")[1].strip())
      green = int(content[line+3].split("__COLORG__")[1].strip())
      blue = int(content[line+4].split("__COLORB__")[1].strip())
      line = line + 5
      for i in range(nb_colors) :
        tmp_visual = []
        while "__ENDVISUAL__" not in content[line] :
          tmp_visual.append(content[line])
          line += 1
        line += 1
        visuals.append(Image.create(tmp_visual,0,0,Color.create_color(red,green,blue)))
    
  npc = create(posx,posy,name,visuals)
  game_inp.npc_list.append(npc)