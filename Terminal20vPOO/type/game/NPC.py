import json
from engine.Image import Image
from engine.Color import Color
import type.game.Character as Character

class NPC(Character.Character):
  def __init__(self, x, y, name, type, visuals, texts, pers_enigma):
    super().__init__(x, y)
    self.__type = type
    self.__name = name
    self.__visuals = visuals
    self.__texts = texts
    self.__enigma = pers_enigma
    self.__special_content = []
  
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
  def get_enigma(self):
    return self.__enigma
  def set_enigma(self,pers_engima):
    self.__enigma = pers_engima
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
    enigma = []
    for line in range(len(content)-1):
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
        dialogue = []
        for h in range(nb_texts) :
          costume = int(content[line].split("__COSTUME__")[1].strip())
          dialogue.append((costume,content[line+1]))
          line += 2
      elif "__QUESTION__" in content[line] : 
        question = content[line].split("__QUESTION__")[1].strip()
        line += 1

        nb_answers = int(content[line].split("__NBREPONSES__")[1].strip())
        line += 1

        answers = []
        for ans in range(nb_answers):
          ans_prop = content[line].split("__REPONSE__")[1].strip()
          line += 1
          if type_npc == 1 :
            nb_blocks = int(content[line].split("__NBBLOCKS__")[1].strip())
            line += 1
            blocks = []
            for bl in range(nb_blocks):
              x, y = int(content[line].split(",")[0]), int(content[line].split(",")[1])
              blocks.append([x,y])
              line += 1
            answers.append([ans_prop, blocks])
          else :
            answers.append(ans_prop)
        enigma = [question, answers]

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
      elif "__CHOICE" in content[line]:
        line += 1
        dialogue_extra = []
        while "__ENDCHOICE__" not in content[line] :
          costume = int(content[line].split("__COSTUME__")[1].strip())
          dialogue_extra.append((costume,content[line+1]))
          line += 2
        special_content[0].append(dialogue_extra)
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

    npc = NPC(posx,posy,name,type_npc,visuals,dialogue,enigma)
    if special_content != [] :
      NPC.set_special_content(npc,special_content)
    game_inp.get_npcs().append(npc)

  def dispatch_NPCS(game_inp, data_path):
    with open(data_path, 'r') as file :
      data = json.load(file)
    npc_elements = data['NPCS']

    for np in npc_elements :
      NPC.upload_NPC_to_game(game_inp,np)