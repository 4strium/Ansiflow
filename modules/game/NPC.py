import json
import time
from modules.engine.Image import Image
from modules.engine.Color import Color
import modules.game.Character as Character
from modules.engine.Buffer import Buffer
import modules.engine.Tools as Tools
from modules.game.Game import Game
from modules.game.memory.MemoryGame import MemoryGame

class NPC(Character.Character):
  def __init__(self, x, y, name, type, visuals, texts):
    super().__init__(x, y)
    self.__type = type
    self.__name = name
    self.__visuals = visuals
    self.__texts = texts
    self.__discuss_choice = -1
    self.__special_content = []
  
  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_type(self):
    return self.__type
  def set_type(self,type):
    self.__type = type
  def get_name(self):
    return self.__name
  def set_name(self,name):
    self.__name = name
  def get_visuals(self):
    return self.__visuals
  def set_visuals(self,visuals):
    self.__visuals = visuals
  def get_texts(self):
    return self.__texts
  def set_texts(self,texts):
    self.__texts = texts
  def get_discuss_choice(self):
    return self.__discuss_choice
  def set_discuss_choice(self,n_dc):
    self.__discuss_choice = n_dc  
  def get_special_content(self):
    return self.__special_content
  def set_special_content(self,special_content):
    self.__special_content = special_content

  def upload_NPC_to_game(game_inp, path):
    try :
      with open(path, 'r', encoding='utf-8') as file_txt:
        tmp = file_txt.readlines()
        content = [line.rstrip('\n') for line in tmp]
    except FileNotFoundError :
      return

    visuals = []
    special_content = [[],[]]
    type_npc = -1
    dialogue = []
    for line in range(len(content)):
      if "__NAME__" in content[line]:
        name = content[line].split("__NAME__")[1].strip()
      elif "__TYPE__" in content[line] :
        type_npc = int(content[line].split("__TYPE__")[1].strip())
      elif "__POSITIONX__" in content[line]:
        posx = float(content[line].split("__POSITIONX__")[1].strip())
      elif "__POSITIONY__" in content[line]:
        posy = float(content[line].split("__POSITIONY__")[1].strip())
      elif "__NBTEXTS__" in content[line]: 
        nb_texts = int(content[line].split("__NBTEXTS__")[1].strip())
        line += 1
        h = 0
        while h < nb_texts :

          if "__CALLFUN__" in content[line] :
            call = content[line].split("__CALLFUN__")[1].strip()
            dialogue.append(('FUNC',call))
            line += 1
            h += 1
          elif "__QUESTION__" in content[line] : 
            blocks_mode = (content[line].split("__QUESTION__")[1].strip() == 'B')
            choice_mode = (content[line].split("__QUESTION__")[1].strip() == 'C')
            line += 1
            question = content[line]
            line += 1

            nb_answers = int(content[line].split("__NBRESPONSES__")[1].strip())
            line += 1

            answers = []
            h += 1
            for ans in range(nb_answers):
              ans_prop = content[line].split("__RESPONSE__")[1].strip()
              line += 1
              if blocks_mode :
                nb_blocks = int(content[line].split("__NBBLOCKS__")[1].strip())
                line += 1
                blocks = []
                for bl in range(nb_blocks):
                  x, y = int(content[line].split(",")[0]), int(content[line].split(",")[1])
                  blocks.append([x,y])
                  line += 1
                answers.append([ans_prop, blocks])
              else :
                answers.append([ans_prop, None])
            if blocks_mode :
              dialogue.append((question, answers, (nb_answers,'B'), -1))
            elif choice_mode :
              dialogue.append((question, answers, (nb_answers,'C'), -1))
            else : 
              dialogue.append((question, answers, (nb_answers,'Z'), -1))
          elif "__CHOICE__" in content[line]:
            num_choice = int(content[line].split("__CHOICE__")[1].strip())
            line += 1
            while "__ENDCHOICE__" not in content[line] :
              costume = int(content[line].split("__COSTUME__")[1].strip())
              dialogue.append((costume,content[line+1],(-1,'Z'),num_choice))
              line += 2
              h += 1
            line+=1
          else :
            costume = int(content[line].split("__COSTUME__")[1].strip())
            dialogue.append((costume,content[line+1],(-1,'Z'), None))
            line += 2
            h += 1

      elif "__VISUAL" in content[line]:
        nb_colors = int(content[line+1].split("__NBCOLORS__")[1].strip())
        line += 2
        colors = []
        for i in range(nb_colors) :
          red = int(content[line].split("__COLORR__")[1].strip())
          green = int(content[line+1].split("__COLORG__")[1].strip())
          blue = int(content[line+2].split("__COLORB__")[1].strip())
          line += 3

          tmp_visual = []
          while "__ENDVISUAL__" not in content[line] :
            tmp_visual.append(content[line])
            line += 1
          line += 1
          colors.append(Image(tmp_visual,0,0,Color(red,green,blue)))
        visuals.append(colors)
      elif "__SPECIALCONTENT__" in content[line]:
        nb_contents = int(content[line].split("__SPECIALCONTENT__")[1].strip())
        line += 1
        for p in range(nb_contents):
          nb_colors = int(content[line].split("__NBCOLORS__")[1].strip())
          line += 1
          colors = []
          for i in range(nb_colors) :
            red = int(content[line].split("__COLORR__")[1].strip())
            green = int(content[line+1].split("__COLORG__")[1].strip())
            blue = int(content[line+2].split("__COLORB__")[1].strip())
            line += 3

            tmp_visual = []
            while "__ENDCONTENT__" not in content[line] :
              tmp_visual.append(content[line])
              line += 1
            line += 1
            colors.append(Image(tmp_visual,0,0,Color(red,green,blue)))
          special_content[1].append(colors)

    npc = NPC(posx,posy,name,type_npc,visuals,dialogue)
    if special_content != [] :
      NPC.set_special_content(npc,special_content)
    game_inp.get_npcs().append(npc)

  def dispatch_NPCS(game_inp, data_path):
    with open(data_path, 'r') as file :
      data = json.load(file)
    npc_elements = data['NPCS']

    for np in npc_elements :
      NPC.upload_NPC_to_game(game_inp,np[1])

  def turn_wheel(window_inp,game_inp,visuals_wheels, text_color):
    Buffer.clear_data(window_inp)
    for color_repartition in visuals_wheels[0]:
      Image.set_pos(color_repartition, [Buffer.get_width(window_inp) // 3, 0])
      Image.draw(color_repartition,window_inp)
    Buffer.set_str_buffer(window_inp, "Appuie sur ESPACE pour tourner la roue",text_color,0, 4, Buffer.get_height(window_inp)//2)
    Buffer.show_data(window_inp)
    while True :
      if Tools.get_key(0.1) == 32 :
        for roundx in range(100):
          Buffer.clear_data(window_inp)
          current_wheel = visuals_wheels[roundx % 5]
          for color_repartition in current_wheel:
            Image.set_pos(color_repartition, [Buffer.get_width(window_inp) // 3, 0])
            Image.draw(color_repartition,window_inp)
          Buffer.show_data(window_inp)
          coeff_time = roundx ** 1.1 # Réduction du coefficient de temps pour accélérer l'arrêt
          if coeff_time > 60:  # Réduction de la limite pour arrêter plus tôt
            break
          time.sleep(Game.get_diff_time(game_inp) * coeff_time)
        time.sleep(4)
        break

  def play_memory(window_inp,game_inp,player_inp,npc,color):
    from main_engine import draw_sentence, open_doors

    time_memory_game = MemoryGame.run_game(window_inp,game_inp,Game.get_color2(game_inp),Game.get_color1(game_inp))
    minutes, seconds = Tools.convert_sec_to_min(time_memory_game)[0], Tools.convert_sec_to_min(time_memory_game)[1]
    sentence_end_memory = (2,"Tu en as mis du temps, "+str(minutes)+"m"+str(seconds)+"s pour ça ?!")
    draw_sentence(window_inp,game_inp,player_inp,npc,sentence_end_memory,color)

    with open(Game.get_datafile(game_inp), 'r') as file :
      data = json.load(file)

    doors_available = data['MemoryGame']['Doors']

    if minutes < 2 :
      open_doors(game_inp,doors_available[0])
    elif minutes < 4 :
      open_doors(game_inp,doors_available[1])
    else :
      open_doors(game_inp,doors_available[2])