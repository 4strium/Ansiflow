import math
import sys
import time
from modules.game.Wall import Wall
from modules.game.Game import Game
from modules.game.Player import Player
from modules.engine.Image import Image
from modules.game.NPC import NPC
from modules.engine.Color import Color
from modules.engine.Button import Button
from modules.engine.Buffer import Buffer
import modules.engine.Tools as Tools
from modules.game.combat.Fight import Fight
from modules.game.combat.Enemy import Enemy
import PyQt6.QtWidgets
from PyQt6.QtCore import Qt

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

def digitalDifferentialAnalyzer(game_inp, angle, x0, y0, max_distance = 30):
  """
    Cette fonction permet de retourner les coordonnées du point d'impact avec un obstacle 
    d'un rayon émis depuis la position (x0,y0) d'un joueur avec un angle spécifié en radians.
    - max-distance correspond à la distance maximale de recherche d'obstacle, 
    si aucun obstacle n'est trouvé la fonction renvoie None
  """

  # Le rayon émis est caractérisé par un vecteur : 
  dx = math.cos(angle) # La composante horizontale, qui correspond au cosinus de l'angle passé en paramètre
  dy = math.sin(angle) # La composante verticale, qui correspond au sinus de l'angle passé en paramètre

  # A ce stade de la fonction nous connaissons donc le point d'accroche du vecteur (x0, y0) ainsi que sa valeur.

  # On détermine dans quelle case de la grille (map) se situe le joueur :
  x_cellule, y_cellule =  int(x0), int(y0)

  # On fixe le pas de déplacement à incrémenter durant la recherche de collision.
  # Si le cosinus de l'angle est positif, cela signifie que l'on va vers la droite.
  # Sinon on va vers la gauche.
  if dx > 0 :
    stepX = 1
  else :
    stepX = -1

  # Si le sinus de l'angle est positif, cela signifie que l'on va vers le haut.
  # Sinon on va vers le bas.
  if dy > 0 :
    stepY = 1
  else :
    stepY = -1

  if dx != 0:
    if dx > 0 :
      next_x = x_cellule + 1 # Abscisse du prochain bord vertical de cellule que le rayon atteindra.
    else :
      next_x = x_cellule # Vu que le rayon va vers la gauche, le prochain axe vertical qu'il va rencontrer est celui à l'origine de la cellule où il se trouve.

    # tmaxX et tmaxY vont nous permettrent de savoir si le rayon atteint en premier le bord de cellule horizontal ou vertical.
    # Ici la première valeur attribuée à tmaxX correspond à la distance entre le point exact du joueur dans la cellule et la première bordure verticale, en empruntant l'axe dx.

    # Ce calcul résulte directement d'une formule trigonométrique de base : hypoténuse = adjacent/cos(angle) 
    # Ici l'hypoténuse c'est la longueur du segment pris sur le rayon entre l'abscisse du joueur et l'abscisse du prochain axe vertical de la grille,
    # le côté adjacent (next_x - x0) c'est la longueur prise entre l'abscisse du joueur et le même axe vertical, mais avec un angle nul cette fois-ci.
    tmaxX = (next_x - x0) / dx 

    tDeltaX = abs(1 / dx) # tDeltaX représente la distance à parcourir entre deux bordures verticales de la grille avec un axe dx
                          # Ici l'hypoténuse c'est la longueur du segment pris entre deux bordures verticales (tDeltaX), et le côté adjacent c'est la longueur d'une cellule : 1
  else:
    tmaxX = float('inf') # Si le cosinus est nul, cela signifie qu'il est impossible d'atteindre la prochaine bordure verticale, que ce soit vers la droite ou vers la gauche.


  # Le raisonnement est le même que pour les abscisses mais avec les ordonnées :
  if dy != 0:
    if dy > 0 :
      next_y = y_cellule + 1
    else :
      next_y = y_cellule

    tmaxY = (next_y - y0) / dy

    tDeltaY = abs(1 / dy) 
  else:
    tmaxY = float('inf')

  distance = 0 # Compteur de la distance parcourue par le rayon depuis la position du joueur
  while distance < max_distance : # Tant que le rayon est inférieur à la distance maximale désignée par l'utilisateur, il continue à explorer les cellules suivantes quie se trouvent sur son cap.
      
    if tmaxX < tmaxY :      # Cette situation a lieu lorsque le rayon touche d'abord l'axe vertical 
      x_cellule += stepX  # On incrémente d'une cellule vers la droite ou vers la gauche (en fonction de la valeur de stepX)

      distance = tmaxX    # La distance correspond donc toujours à : (nombre de cellules traversées depuis la position du joueur) × (la distance nécessaire pour traverser une cellule) + distance entre le joueur et la première bordure.
      tmaxX += tDeltaX
    else :                  # Cette situation a lieu lorsque le rayon touche d'abord l'axe horizontal (le raisonnement est identique au cas précédent mais verticalement ici)
      y_cellule += stepY
      distance = tmaxY
      tmaxY += tDeltaY
    
    if 0 <= x_cellule < len(Game.get_map(game_inp)[0]) and 0 <= y_cellule < len(Game.get_map(game_inp)) :
      if Game.get_map(game_inp)[y_cellule][x_cellule] == 1:

        # On calcule les coordonnées exactes du point d'impact en fonction du déplacement du rayon :
        impact_x = x0 + distance * dx
        impact_y = y0 + distance * dy
            
        return (impact_x, impact_y, distance)

  return None

def draw3DWall(window, game_inp, ray_distance, player_angle, ray_angle, wall_design) :
  # Correction de l'effet "fish-eye" :
  angle_fix = player_angle - ray_angle
  if angle_fix < 0 :
   angle_fix += 2*PI
  elif angle_fix > 2*PI :
   angle_fix -= 2*PI
  ray_distance = ray_distance * math.cos(angle_fix)

  if ray_distance < 0.1 :
    ray_distance = 0.1

  lineHeight = window.getHeight() / ray_distance
  if lineHeight > window.getHeight() :
    lineHeight = window.getHeight()

  center_h = window.getHeight() // 2 
  y_start = center_h - (lineHeight //2)

  for y_axis in range(round(y_start), round(y_start + lineHeight)) :
    if 0 <= y_axis < window.getHeight()-1:
      for i in range(round(Wall.get_start_ind(wall_design)), Wall.get_end_ind(wall_design)) :
        if 0 <= i < window.getWidth():
          if i == Wall.get_end_ind(wall_design)-1 :
            Buffer.set_str_buffer(window, " ", Game.get_color2(game_inp), 400, i, y_axis)
          else :
            Buffer.set_str_buffer(window, Wall.get_texture(wall_design), Wall.get_color(wall_design), ray_distance, i, y_axis)

def drawFloor(window, game_inp) :
  for y_axis in range(window.getHeight()//2, window.getHeight()) :
    if 0 <= y_axis < window.getHeight() -1 :
      for x_axis in range(0, window.getWidth()) :
        Buffer.set_str_buffer(window, "-", Game.get_color2(game_inp), 30, x_axis, y_axis)

def get_rays(window, game_inp, player) :
  """
    Procédure qui génère des rayons à partir de la position du joueur (pos_x, pos_y).
    - angle_init : angle en radians situé en plein milieu du champ de vision
    - fov : champ de vision en degrés.
    Pour la valeur par défaut, 60°, l'algorithme trace donc des rayons de collision sur un angle de 30° à gauche de "angle_init", ainsi que sur 30° à droite de "angle_init".
  """

  width = window.getWidth()
  fov_deg = Player.get_fov(player)
  fov_rad = math.radians(fov_deg)

  angle_acc = Player.get_left_angle(player)
  angle_step = fov_rad / width    # un rayon par pixel
  px, py = Player.get_position(player)

  for x in range(width) :
    res = digitalDifferentialAnalyzer(game_inp,angle_acc, px, py)
    if res != None :
      wall_design = Wall(Game.get_color1(game_inp),"█",x, 1)
      draw3DWall(window, game_inp, res[2], Player.get_angle(player), angle_acc, wall_design)

    angle_acc -= angle_step

def endGame(emu_terminal, game, death):
  x_start = emu_terminal.getWidth() // 16
  y_start = emu_terminal.getHeight() // 30

  emu_terminal.clearBuffer()

  if death == 0:
    skull = Image.upload_classic_image(Game.get_death_path(game), x_start, y_start, Game.get_color1(game))
    Image.set_color(skull,Color(255,0,255))
    Image.draw(skull, emu_terminal)
  elif death == 1:
    text_end = Image.upload_classic_image(Game.get_ending_path(game), 0, 0, Game.get_color2(game))
    Image.draw(text_end, emu_terminal)

  emu_terminal.showBuffer()
  sys.exit()
  exit()

def open_doors(game_inp, lst_blocks):
  for bloob in range(len(lst_blocks)): 
    Game.get_map(game_inp)[lst_blocks[bloob][1]][lst_blocks[bloob][0]] = 0

def draw_backtalk(window_inp, color):
  for i in range(window_inp.getWidth()):
    Buffer.set_str_buffer(window_inp,"─",color,0.1,i,(window_inp.getHeight() // 3)*2)
  for j in range((window_inp.getHeight() // 3)*2+1,window_inp.getHeight()-1):
    for k in range(window_inp.getWidth()):
      Buffer.set_str_buffer(window_inp," ",color,0.1,k,j)

def draw_sentence(window_inp, game_inp, player_inp, npc, sentence, color):
  window_inp.clearBuffer()
  get_rays(window_inp, game_inp, player_inp)
  draw_backtalk(window_inp, color)
  for i in range(len(NPC.get_visuals(npc)[sentence[0] - 1])):
    Image.set_pos(NPC.get_visuals(npc)[sentence[0] - 1][i], [window_inp.getWidth() // 2, -2])
    Image.draw(NPC.get_visuals(npc)[sentence[0] - 1][i], window_inp)
  window_inp.showBuffer()
  PyQt6.QtWidgets.QApplication.processEvents()

  padding = 12
  x_index = padding
  y_line = (window_inp.getHeight() // 4) * 3
  text = sentence[1]

  for letter in text:
    if x_index < window_inp.getWidth() - padding:
      if x_index > ((window_inp.getWidth() // 2) - 6):
        if letter == ' ':
          x_index = padding - 1
          y_line += 1
      Buffer.set_str_buffer(window_inp, letter, color, 0, x_index, y_line)
      x_index += 1
      window_inp.showBuffer()
      PyQt6.QtWidgets.QApplication.processEvents() 
      time.sleep(0.01)
  
  time.sleep(2)

def annotations_user(window_inp, color):
  Buffer.set_str_buffer(window_inp, "Utilise Q et D pour changer de réponse", color,0, window_inp.getWidth()-45, window_inp.getHeight()-8)
  Buffer.set_str_buffer(window_inp, "Appuie sur ESPACE pour confirmer ta réponse",color,0, window_inp.getWidth()-48, window_inp.getHeight()-7)

def ask_question(window_inp, game_inp, npc, sentence, color):
  padding = 12
  x_shift = 60
  nb_buttons = sentence[2][0]
  button_lst = [Button(sentence[1][i][0],[padding + i*x_shift, (window_inp.getHeight()//5)*4],Game.get_color2(game_inp), Game.get_color1(game_inp)) for i in range(nb_buttons)]

  draw_backtalk(window_inp, color)
  Buffer.set_str_buffer(window_inp, sentence[0], color, 0, padding, (window_inp.getHeight()//4)*3)
  window_inp.showBuffer()
  PyQt6.QtWidgets.QApplication.processEvents()

  choice = 0 
  annotations_user(window_inp, color)
  key = None

  while True:
    for idx, btn in enumerate(button_lst):
      Button.draw_text_button(btn, window_inp, idx == choice)

    key = window_inp.getKey()

    if key == Qt.Key.Key_D and choice + 1 < nb_buttons:
      choice += 1
    elif key == Qt.Key.Key_Q and choice - 1 >= 0:
      choice -= 1
    elif key == Qt.Key.Key_Space: 
      if sentence[2][1] == 'B':
        open_doors(game_inp, sentence[1][choice][1])
      elif sentence[2][1] == 'C' :
        NPC.set_discuss_choice(npc,choice+1)
      break

    window_inp.showBuffer()
    PyQt6.QtWidgets.QApplication.processEvents()

  window_inp.clearBuffer()
  PyQt6.QtWidgets.QApplication.processEvents()

def talk_to_NPC(window_inp,player_inp,game_inp,npc,color):
  for sentence in NPC.get_texts(npc) :
    if sentence[0] == 'FUNC':
      window_inp.clearBuffer()
      eval(sentence[1])
      window_inp.clearBuffer()
    elif sentence[2][0] != -1 :
      get_rays(window_inp, game_inp, player_inp)
      ask_question(window_inp,game_inp,npc,sentence,color)
    elif (sentence[3] != None and sentence[3] == NPC.get_discuss_choice(npc)) or sentence[3] == None :
      draw_sentence(window_inp,game_inp,player_inp,npc,sentence,color)
  
  if NPC.get_type(npc) == 3 :
    endGame(window_inp,game_inp,1)

  Game.get_npcs(game_inp).remove(npc)   

def draw_NPC(window_inp, game_inp, player_inp, talk_color):
  for npc_g in game_inp.get_npcs() :
    distance = math.sqrt((NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0])**2+(NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])**2)

    if distance < 6 :
      Buffer.set_str_buffer(window_inp, str(round(distance,3)), talk_color, 0, window_inp.getWidth() // 2, 0)
      Buffer.set_str_buffer(window_inp, str(NPC.get_name(npc_g)), talk_color, 0, window_inp.getWidth() // 2, 1)

    if 0.01 < distance < 2.5 :
      if distance > 1 :
        vector_origin = (math.cos(Player.get_angle(player_inp)),math.sin(Player.get_angle(player_inp)))
        vector_NPC = (NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0], NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])
        angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

        fov_limits = (Player.get_fov(player_inp)//2)*INCREMENT_RAD
        x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * window_inp.getWidth())

        if -fov_limits <= angle_player_npc <= fov_limits :
          for i in range(len(NPC.get_visuals(npc_g)[0])):
            Image.set_pos(NPC.get_visuals(npc_g)[0][i],[x_fix,2])
            Image.draw(NPC.get_visuals(npc_g)[0][i],window_inp,distance)
      else :
        draw_backtalk(window_inp, talk_color)
        talk_to_NPC(window_inp, player_inp, game_inp, npc_g, talk_color)
