import numpy as np
import math
import curses
import time
import type.game.Player_Window as P_win
import type.game.Wall as Wall
import type.game.Game as Game
import type.game.Player as Player
import type.game.Image as Image
import type.game.NPC as NPC
import engine.Color as Color
import engine.Button as Button

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

GREEN_MATRIX = (0, 233, 2)

wall_pink = 0
blue_cyber = 0

# Exemple de carte (map)
map = np.array(
  [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #37
    [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1], #36
    [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,1], #35
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1], #34
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1], #33
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1], #32
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,0,0,1,0,1], #31
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1,0,1], #30
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,0,0,0,0,0,0,1], #29
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1], #28
    [1,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1], #27
    [1,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1], #26
    [1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1], #25
    [1,0,1,1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,0,1], #24
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,1], #23
    [1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,1,1,0,1], #22
    [1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,1], #21
    [1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,1,1,0,1,1,1], #20
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1], #19
    [1,0,1,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,0,1,1,1,0,1], #18
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,1,1,1,0,1], #17
    [1,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1], #16
    [1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,1,1,1,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,1,0,1], #15
    [1,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,0,1], #14
    [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,1], #13
    [1,0,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,0,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1], #12
    [1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,0,1,0,1,0,1,0,1], #11
    [1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1], #10
    [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1], #9
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1], #8
    [1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1,0,0,0,0,0,1], #7
    [1,0,1,0,1,0,0,0,1,0,1,1,0,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1,0,0,0,0,0,1], #6
    [1,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1], #5
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,1,1,1,0,0,0,1], #4
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,0,1,1,0,1,0,0,0,1,1,1,0,1], #3 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1], #2
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1], #1
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  #0
  ]
)

reversed_map = np.flipud(map)

def digitalDifferentialAnalyzer(angle, x0, y0, max_distance = 10):
    """
    Cette fonction permet de retourner les coordonnées du point d'impact avec un obstacle 
    d'un rayon émis depuis la position (x0,y0) d'un joueur avec un angle spécifié en radians.
    - max-distance correspond à la distance maximale de recherhe d'obstacle, 
    si aucun obstacle n'est trouvé la fonction renvoie None
    """

    global reversed_map

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
        
        if 0 <= x_cellule <= map.shape[1] and 0 <= y_cellule <= map.shape[0] :
            if reversed_map[y_cellule][x_cellule] == 1:

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

  lineHeight = P_win.get_height(window) / ray_distance
  if lineHeight > P_win.get_height(window) :
    lineHeight = P_win.get_height(window)

  center_h = P_win.get_height(window) // 2 
  y_start = center_h - (lineHeight //2)

  for y_axis in range(round(y_start), round(y_start + lineHeight)) :
    if 0 <= y_axis < P_win.get_height(window)-1:
      for i in range(round(Wall.get_start_ind(wall_design)), Wall.get_end_ind(wall_design)) :
        if 0 <= i < P_win.get_width(window):
          if i == Wall.get_end_ind(wall_design)-1 :
            P_win.get_stdscr(window).addstr(y_axis, i, " ")
          else :
            P_win.get_stdscr(window).addstr(y_axis, i, Wall.get_texture(wall_design), Wall.get_color(wall_design))

def drawFloor(window) :
  for y_axis in range(P_win.get_height(window)//2, P_win.get_height(window)) :
    if 0 <= y_axis < P_win.get_height(window) -1 :
      for x_axis in range(0, P_win.get_width(window)) :
        P_win.get_stdscr(window).addstr(y_axis, x_axis, "-")

def get_rays(window, player) :
    """
    Procédure qui génère des rayons à partir de la position du joueur (pos_x, pos_y).
    - angle_init : angle en radians situé en plein milieu du champ de vision
    - fov : champ de vision en degrés.
    Pour la valeur par défaut, 60°, l'algorithme trace donc des rayons de collision sur un angle de 30° à gauche de "angle_init", ainsi que sur 30° à droite de "angle_init".
    """

    angle_acc = Player.get_left_angle(player)
    increment_width = P_win.get_width(window) / Player.get_fov(player)
    counter_x = 0 

    for i in range(0,Player.get_fov(player)+1) :
        res = digitalDifferentialAnalyzer(angle_acc, Player.get_position(player)[0], Player.get_position(player)[1])
        if res != None :
          wall_design = Wall.create(wall_pink,"█",counter_x, increment_width)
          draw3DWall(window, res[2], Player.get_angle(player), angle_acc, wall_design)

        angle_acc -= INCREMENT_RAD
        counter_x = round(i * increment_width)

def endGame(window, death):

  x_start = P_win.get_width(window) // 16
  y_start = P_win.get_height(window) // 30

  skull = Image.upload_classic_image('images/skull.txt', x_start, y_start, wall_pink)
  Image.set_color(skull,Color.create_color(255,0,255))
  Image.draw(window, skull)

  if death == 0:
    text_walls = Image.upload_classic_image('text/walls.txt', int(P_win.get_width(window)*0.48), int(P_win.get_height(window)*0.24), blue_cyber)
    Image.draw(window, text_walls)

  P_win.get_stdscr(window).refresh()
  time.sleep(10)

def open_doors(lst_blocks):
  global reversed_map

  for bloob in len(lst_blocks)-1: 
    reversed_map[lst_blocks[bloob][1]][lst_blocks[bloob][0]]

def talk_to_NPC(window_inp,player_inp,game_inp,npc,color):
  for sentence in NPC.get_texts(npc) :
    for i in range(len(NPC.get_visuals(npc)[sentence[0]])):
      Image.set_pos(npc.visuals[sentence[0]][i],[P_win.get_width(window_inp) // 2,(P_win.get_height(window_inp) // 8)])
      Image.draw(window_inp, NPC.get_visuals(npc)[sentence[0]][i])
    P_win.get_stdscr(window_inp).refresh()
    
    padding = 12
    x_index = padding
    for letter in sentence[1] :
      if x_index < P_win.get_width(window_inp) - padding :
        P_win.get_stdscr(window_inp).addstr((P_win.get_height(window_inp) // 4)*3, x_index, letter, color)
        x_index += 1
        P_win.get_stdscr(window_inp).refresh()
        time.sleep(Game.get_diff_time(game_inp)*8)
    time.sleep(4)
    P_win.get_stdscr(window_inp).clear()
    get_rays(window_inp, player_inp)
    Game.draw_backtalk(window_inp, color)
  P_win.get_stdscr(window_inp).addstr((P_win.get_height(window_inp) // 4)*3, padding, NPC.get_enigma(npc)[0], color)
  P_win.get_stdscr(window_inp).refresh()
  time.sleep(8)
  x_shift = 60
  button_lst = []
  for butt in range(3):
    button_tmp = Button.create(NPC.get_enigma(npc)[1][butt][0], [padding+butt*x_shift,(P_win.get_height(window_inp) // 5)*4], blue_cyber, wall_pink)
    button_lst.append(button_tmp)
  choice = 1
  while True :
    key = P_win.get_stdscr(window_inp).getch()

    if choice == 1 :
      Button.draw_button(window_inp,button_lst[0],1)
      Button.draw_button(window_inp,button_lst[1],0)
      Button.draw_button(window_inp,button_lst[2],0)
      if key == ord('d') :
        choice += 1
    elif choice == 2 :
      Button.draw_button(window_inp,button_lst[0],0)
      Button.draw_button(window_inp,button_lst[1],1)
      Button.draw_button(window_inp,button_lst[2],0)
      if key == ord('d') :
        choice += 1
      elif key == ord('q') :
        choice -= 1
    else :
      Button.draw_button(window_inp,button_lst[0],0)
      Button.draw_button(window_inp,button_lst[1],0)
      Button.draw_button(window_inp,button_lst[2],1)
      if key == ord('q') :
        choice -= 1
    P_win.get_stdscr(window_inp).addstr(P_win.get_height(window_inp)-5, x_shift+2, "Utilise Q et D pour changer de réponse", color)
    P_win.get_stdscr(window_inp).addstr(P_win.get_height(window_inp)-3, x_shift, "Appuie sur ESPACE pour confirmer ta réponse", color)
    P_win.get_stdscr(window_inp).refresh()
    time.sleep(Game.get_diff_time(game_inp))

def draw_NPC(window_inp, game_inp, player_inp, talk_color):
  for npc_g in game_inp.npc_list :
    distance = math.sqrt((NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0])**2+(NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])**2)

    if distance < 10 :
      P_win.get_stdscr(window_inp).addstr(0, P_win.get_width(window_inp) // 2, str(round(distance,3)), 1)
      P_win.get_stdscr(window_inp).addstr(1, P_win.get_width(window_inp) // 2, str(game_inp.npc_list[0].name), 1)

    if 0.01 < distance < 2.5 :
      if distance > 1 :
        vector_origin = (math.cos(Player.get_angle(player_inp)),math.sin(Player.get_angle(player_inp)))
        vector_NPC = (NPC.get_position(npc_g)[0] - Player.get_position(player_inp)[0], NPC.get_position(npc_g)[1] - Player.get_position(player_inp)[1])
        angle_player_npc = math.atan2(vector_origin[0]*vector_NPC[1] - vector_origin[1]*vector_NPC[0],vector_origin[0]*vector_NPC[0] + vector_origin[1]*vector_NPC[1])

        fov_limits = (Player.get_fov(player_inp)//2)*INCREMENT_RAD
        x_fix = int(((fov_limits - angle_player_npc) / (2 * fov_limits)) * P_win.get_width(window_inp))

        if -fov_limits <= angle_player_npc <= fov_limits :
          for i in range(len(NPC.get_visuals(npc_g)[0])):
            Image.set_pos(npc_g.visuals[0][i],[x_fix,(P_win.get_height(window_inp) // 4)])
            Image.draw(window_inp, NPC.get_visuals(npc_g)[0][i])
        P_win.get_stdscr(window_inp).addstr(2, P_win.get_width(window_inp) // 2, str(angle_player_npc), 1)
      else :
        Game.draw_backtalk(window_inp, talk_color)
        talk_to_NPC(window_inp, player_inp, game_inp, npc_g, talk_color)

def run(stdscr):
  global wall_pink, blue_cyber, reversed_map

  curses.curs_set(0) #Masquer le curseur

  window = P_win.create(stdscr)
  P_win.get_stdscr(window).nodelay(1)
  P_win.get_stdscr(window).timeout(100) #Faire varier le rafraichissement du terminal en ms 

  # Démarrage du gestionnaire de couleurs :
  curses.start_color()
  wall_pink = Color.create_color(189, 0, 255)
  blue_cyber = Color.create_color(0,255,159)

  
  game_run = Game.create(0.01,reversed_map)
  player_run = Player.create([17.5, 16.5], 80)

  NPC.upload_NPC_to_game(game_run, "images/NPCS/chuck.txt")

  while True :
    P_win.refresh_size(window)

    if reversed_map[int(Player.get_position(player_run)[1])][int(Player.get_position(player_run)[0])] :
      P_win.get_stdscr(window).erase()
      P_win.get_stdscr(window).refresh()
      endGame(window, 0)
      break

    Player.move(player_run,Game.get_diff_time(game_run),window)
    drawFloor(window)
    get_rays(window, player_run)

    draw_NPC(window,game_run,player_run,blue_cyber)

    Game.running_time(game_run)
    time.sleep(Game.get_diff_time(game_run)) # Faire varier le rafraichissment des animations
    
curses.wrapper(run)