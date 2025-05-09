import math
import termios
import sys
import tty
import time
import json
import type.game.Wall as Wall
import type.game.Game as Game
import type.game.Player as Player
import engine.Image as Image
import type.game.NPC as NPC
import engine.Color as Color
import engine.Button as Button
import engine.Buffer as Buffer
import engine.Tools as Tools
import type.game.memory.MemoryGame as MemoryGame
import type.game.combat.Fight as Fight
import type.game.combat.Enemy as Enemy

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

GREEN_MATRIX = (0, 233, 2)

wall_pink = 0
blue_cyber = 0

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

def draw3DWall(window, ray_distance, player_angle, ray_angle, wall_design) :
  # Correction de l'effet "fish-eye" :
  angle_fix = player_angle - ray_angle
  if angle_fix < 0 :
   angle_fix += 2*PI
  elif angle_fix > 2*PI :
   angle_fix -= 2*PI
  ray_distance = ray_distance * math.cos(angle_fix)

  if ray_distance < 0.1 :
    ray_distance = 0.1

  lineHeight = Buffer.get_height(window) / ray_distance
  if lineHeight > Buffer.get_height(window) :
    lineHeight = Buffer.get_height(window)

  center_h = Buffer.get_height(window) // 2 
  y_start = center_h - (lineHeight //2)

  for y_axis in range(round(y_start), round(y_start + lineHeight)) :
    if 0 <= y_axis < Buffer.get_height(window)-1:
      for i in range(round(Wall.get_start_ind(wall_design)), Wall.get_end_ind(wall_design)) :
        if 0 <= i < Buffer.get_width(window):
          if i == Wall.get_end_ind(wall_design)-1 :
            Buffer.set_str_buffer(window, " ", blue_cyber, 400, i, y_axis)
          else :
            Buffer.set_str_buffer(window, Wall.get_texture(wall_design), Wall.get_color(wall_design), ray_distance, i, y_axis)

def drawFloor(window) :
  global blue_cyber
  for y_axis in range(Buffer.get_height(window)//2, Buffer.get_height(window)) :
    if 0 <= y_axis < Buffer.get_height(window) -1 :
      for x_axis in range(0, Buffer.get_width(window)) :
        Buffer.set_str_buffer(window, "-", blue_cyber, 30, x_axis, y_axis)

def get_rays(window, game_inp, player) :
    """
    Procédure qui génère des rayons à partir de la position du joueur (pos_x, pos_y).
    - angle_init : angle en radians situé en plein milieu du champ de vision
    - fov : champ de vision en degrés.
    Pour la valeur par défaut, 60°, l'algorithme trace donc des rayons de collision sur un angle de 30° à gauche de "angle_init", ainsi que sur 30° à droite de "angle_init".
    """

    width   = Buffer.get_width(window)
    fov_deg = Player.get_fov(player)
    fov_rad = math.radians(fov_deg)

    angle_acc   = Player.get_left_angle(player)
    angle_step  = fov_rad / width    # un rayon par pixel
    px, py      = Player.get_position(player)

    for x in range(width) :
        res = digitalDifferentialAnalyzer(game_inp,angle_acc, px, py)
        if res != None :
          wall_design = Wall.create(wall_pink,"█",x, 1)
          draw3DWall(window, res[2], Player.get_angle(player), angle_acc, wall_design)

        angle_acc -= angle_step

def endGame(window, death):

  x_start = Buffer.get_width(window) // 16
  y_start = Buffer.get_height(window) // 30

  skull = Image.upload_classic_image('images/skull.txt', x_start, y_start, wall_pink)
  Image.set_color(skull,Color.create_color(255,0,255))
  Image.draw(window, skull)

  if death == 0:
    text_walls = Image.upload_classic_image('text/walls.txt', int(Buffer.get_width(window)*0.48), int(Buffer.get_height(window)*0.24), blue_cyber)
    Image.draw(window, text_walls)

  Buffer.show_data(window)
  time.sleep(10)

def open_doors(game_inp, lst_blocks):
  for bloob in range(len(lst_blocks)): 
    Game.get_map(game_inp)[lst_blocks[bloob][1]][lst_blocks[bloob][0]] = 0

def turn_wheel(window_inp,game_inp,visuals_wheels, text_color):
  Buffer.clear_data(window_inp)
  for color_repartition in visuals_wheels[0]:
    Image.set_pos(color_repartition, [Buffer.get_width(window_inp) // 3, 0])
    Image.draw(window_inp, color_repartition)
  Buffer.set_str_buffer(window_inp, "Appuie sur ESPACE pour tourner la roue",text_color,0, 4, Buffer.get_height(window_inp)//2)
  Buffer.show_data(window_inp)
  while True :
    if Tools.get_key() == 32 :
      for roundx in range(100):
        Buffer.clear_data(window_inp)
        current_wheel = visuals_wheels[roundx % 5]
        for color_repartition in current_wheel:
          Image.set_pos(color_repartition, [Buffer.get_width(window_inp) // 3, 0])
          Image.draw(window_inp, color_repartition)
        Buffer.show_data(window_inp)
        coeff_time = roundx ** 1.1 # Réduction du coefficient de temps pour accélérer l'arrêt
        if coeff_time > 60:  # Réduction de la limite pour arrêter plus tôt
          break
        time.sleep(Game.get_diff_time(game_inp) * coeff_time)
      time.sleep(4)
      break

def draw_sentence(window_inp,game_inp,player_inp,npc,sentence,color):
  get_rays(window_inp, game_inp, player_inp)
  Game.draw_backtalk(window_inp, color) 
  for i in range(len(NPC.get_visuals(npc)[sentence[0]])):
    Image.set_pos(npc.visuals[sentence[0]][i],[Buffer.get_width(window_inp) // 2,-2])
    Image.draw(window_inp, NPC.get_visuals(npc)[sentence[0]][i])
  Buffer.show_data(window_inp)

  padding = 12
  x_index = padding
  y_line = (Buffer.get_height(window_inp) // 4)*3
  for letter in sentence[1] :
    if x_index < Buffer.get_width(window_inp) - padding :
      if x_index > ((Buffer.get_width(window_inp)//2)-6) :
        if letter == ' ' :
          x_index = padding-1
          y_line += 1
      Buffer.set_str_buffer(window_inp, letter, color,0, x_index, y_line)
      x_index += 1
      Buffer.show_data(window_inp)
      time.sleep(Game.get_diff_time(game_inp)*8)
  time.sleep(4)
  Buffer.clear_data(window_inp)

def response_wheel(window_inp,game_inp,player_inp,npc,sentence,color, statement):
  Buffer.clear_data(window_inp)
  for sentence in NPC.get_special_content(npc)[0][statement] :
    draw_sentence(window_inp,game_inp,player_inp,npc,sentence,color)
  turn_wheel(window_inp, game_inp, NPC.get_special_content(npc)[1],color)
  Buffer.clear_data(window_inp)
  ending_sentence = (2,"28 CARTES IHIHIHIHIHIHIH QUEL DOMMAGE FRANCHEMENT...")
  draw_sentence(window_inp,game_inp,player_inp,npc,ending_sentence,color)
  time.sleep(2)

def play_memory(window_inp,game_inp,player_inp,npc,color):
  time_memory_game = MemoryGame.run_game(window_inp,game_inp,blue_cyber,wall_pink)
  minutes, seconds = Tools.convert_sec_to_min(time_memory_game)[0], Tools.convert_sec_to_min(time_memory_game)[1]
  sentence_end_memory = (2,"Tu en as mis du temps, "+str(minutes)+"m"+str(seconds)+"s pour ça ?!")
  draw_sentence(window_inp,game_inp,player_inp,npc,sentence_end_memory,color)

  with open(game_inp.datafile, 'r') as file :
    data = json.load(file)

  doors_available = data['MemoryGame']['Doors']

  if minutes < 2 :
    open_doors(game_inp,doors_available[0])
  elif minutes < 4 :
    open_doors(game_inp,doors_available[1])
  else :
    open_doors(game_inp,doors_available[2])  

  Game.get_npcs(game_inp).remove(npc)

def annotations_user(window_inp, color):
  Buffer.set_str_buffer(window_inp, "Utilise Q et D pour changer de réponse", color,0, Buffer.get_width(window_inp)-45, Buffer.get_height(window_inp)-8)
  Buffer.set_str_buffer(window_inp, "Appuie sur ESPACE pour confirmer ta réponse",0, color, Buffer.get_width(window_inp)-48, Buffer.get_height(window_inp)-7)
  Buffer.show_data(window_inp)

def talk_to_NPC(window_inp,player_inp,game_inp,npc,color):

  padding = 12

  for sentence in NPC.get_texts(npc) :
    draw_sentence(window_inp,game_inp,player_inp,npc,sentence,color)
  get_rays(window_inp, game_inp, player_inp)
  Game.draw_backtalk(window_inp, color)
  Buffer.set_str_buffer(window_inp, NPC.get_enigma(npc)[0], color, 0, padding,(Buffer.get_height(window_inp) // 4)*3)
  Buffer.show_data(window_inp)
  time.sleep(4)

  if NPC.get_type(npc) == 1 :
    x_shift = 60
    button_lst = []
    for butt in range(3):
      button_tmp = Button.create(NPC.get_enigma(npc)[1][butt][0], [padding+butt*x_shift,(Buffer.get_height(window_inp) // 5)*4], blue_cyber, wall_pink)
      button_lst.append(button_tmp)
    choice = 1
    key = None

    while True :

      if choice == 1 :
        Button.draw_text_button(window_inp,button_lst[0],1)
        Button.draw_text_button(window_inp,button_lst[1],0)
        Button.draw_text_button(window_inp,button_lst[2],0)
        if key == ord('d') :
          choice += 1
        elif key == 32 :
          open_doors(game_inp,NPC.get_enigma(npc)[1][0][1])
          Game.get_npcs(game_inp).remove(npc)
          break       
      elif choice == 2 :
        Button.draw_text_button(window_inp,button_lst[0],0)
        Button.draw_text_button(window_inp,button_lst[1],1)
        Button.draw_text_button(window_inp,button_lst[2],0)
        if key == ord('d') :
          choice += 1
        elif key == ord('q') :
          choice -= 1
        elif key == 32 :
          open_doors(game_inp,NPC.get_enigma(npc)[1][1][1])
          Game.get_npcs(game_inp).remove(npc)
          break
      else :
        Button.draw_text_button(window_inp,button_lst[0],0)
        Button.draw_text_button(window_inp,button_lst[1],0)
        Button.draw_text_button(window_inp,button_lst[2],1)
        if key is None :
          pass
        elif key == ord('q') :
          choice -= 1
        elif key == 32 :
          open_doors(game_inp,NPC.get_enigma(npc)[1][2][1])
          Game.get_npcs(game_inp).remove(npc)
          break
      annotations_user(window_inp,color)
      key = Tools.get_key()
      time.sleep(Game.get_diff_time(game_inp))
  elif NPC.get_type(npc) == 2 :
    x_shift = 60
    button_lst = []

    for butt in range(2):
      button_tmp = Button.create(NPC.get_enigma(npc)[1][butt], [padding+butt*x_shift,(Buffer.get_height(window_inp) // 5)*4], blue_cyber, wall_pink)
      button_lst.append(button_tmp)
    choice = 1
    key = None

    while True :

      if choice == 1 :
        Button.draw_text_button(window_inp,button_lst[0],1)
        Button.draw_text_button(window_inp,button_lst[1],0)
        if key == ord('d') :
          choice += 1
        elif key == 32 :
          response_wheel(window_inp,game_inp,player_inp,npc,sentence,color,0)
          play_memory(window_inp,game_inp,player_inp,npc,color)
          break
      else :
        Button.draw_text_button(window_inp,button_lst[0],0)
        Button.draw_text_button(window_inp,button_lst[1],1)
        if key == ord('q') :
          choice -= 1
        elif key == 32 :
          response_wheel(window_inp,game_inp,player_inp,npc,sentence,color,1)
          play_memory(window_inp,game_inp,player_inp,npc,color)
          break
      annotations_user(window_inp,color)
      key = Tools.get_key()
      time.sleep(Game.get_diff_time(game_inp))
     

def draw_NPC(window_inp, game_inp, player_inp, talk_color):
  for npc_g in game_inp.npc_list :
    distance = math.sqrt((NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0])**2+(NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])**2)

    if distance < 10 :
      Buffer.set_str_buffer(window_inp, str(round(distance,3)), talk_color, 0, Buffer.get_width(window_inp) // 2, 0)
      Buffer.set_str_buffer(window_inp, str(NPC.get_name(npc_g)), talk_color, 0, Buffer.get_width(window_inp) // 2, 1)

    if 0.01 < distance < 2.5 :
      if distance > 1 :
        vector_origin = (math.cos(Player.get_angle(player_inp)),math.sin(Player.get_angle(player_inp)))
        vector_NPC = (NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0], NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])
        angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

        fov_limits = (Player.get_fov(player_inp)//2)*INCREMENT_RAD
        x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * Buffer.get_width(window_inp))

        if -fov_limits <= angle_player_npc <= fov_limits :
          for i in range(len(NPC.get_visuals(npc_g)[0])):
            Image.set_pos(npc_g.visuals[0][i],[x_fix,2])
            Image.draw(window_inp, NPC.get_visuals(npc_g)[0][i],distance)
        Buffer.set_str_buffer(window_inp, str(angle_player_npc),talk_color, 0, Buffer.get_width(window_inp) // 2, 2)
      else :
        Game.draw_backtalk(window_inp, talk_color)
        talk_to_NPC(window_inp, player_inp, game_inp, npc_g, talk_color)

def refresh_buffer(buffer_inp) :
  # Création du buffer :
  rows, cols = termios.tcgetwinsize(sys.stdout.fileno())
  Buffer.clear_data(buffer_inp)
  Buffer.set_height(buffer_inp, rows)
  Buffer.set_width(buffer_inp, cols)

def run():
  global wall_pink, blue_cyber

  # Démarrage du gestionnaire de couleurs :
  wall_pink = Color.create_color(189, 0, 255)
  blue_cyber = Color.create_color(0,255,159)

  rows, cols = termios.tcgetwinsize(sys.stdout.fileno())
  buffer_window = Buffer.create(cols, rows)

  game_run = Game.create(0.01, "data.json", termios.tcgetattr(sys.stdin))
  tty.setcbreak(sys.stdin.fileno())
  player_run = Player.create([33.5, 23], 80)

  NPC.dispatch_NPCS(game_run,"data.json")

  fight_game = Fight.create(buffer_window)
  Enemy.dispatch_Enemies(fight_game,"data.json")

  while True :
    key = Tools.get_key()

    if key == 27:  # Quitter avec 'échap'
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, Game.get_backup_terminal(game_run))
      sys.exit()
      exit()

    refresh_buffer(buffer_window)

    if Game.get_map(game_run)[int(Player.get_position(player_run)[1])][int(Player.get_position(player_run)[0])] :
      refresh_buffer(buffer_window)
      endGame(buffer_window, 0)
      break

    Player.move(game_run,player_run,buffer_window,key)
    drawFloor(buffer_window)
    get_rays(buffer_window, game_run, player_run)

    draw_NPC(buffer_window,game_run,player_run,blue_cyber)

    if Fight.is_fight_time(fight_game,player_run)[0] :
      Enemy.draw_Enemy(buffer_window,fight_game,player_run,blue_cyber)
      Fight.update_fight(buffer_window,fight_game,blue_cyber)
      if key == 32 :
        fight_game.flame_state = 10
        Enemy.shoot_ennemy(buffer_window,Fight.is_fight_time(fight_game,player_run)[1],fight_game)

    Buffer.show_data(buffer_window)

    Game.running_time(game_run)
    time.sleep(Game.get_diff_time(game_run)) # Faire varier le rafraichissment des animations
    
if __name__ == "__main__":
  run()