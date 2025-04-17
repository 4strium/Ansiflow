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

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

GREEN_MATRIX = (0, 233, 2)

# Exemple de carte (map)
map = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],    # [1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1]
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],    # [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1]
    [1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1],    # [1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1]
    [1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1],    # [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1]
    [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],    # [1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1]
    [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],    # [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1]
    [1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],    # [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1],    # [1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1]
    [1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1],    # [1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1]
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],    # [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1]
    [1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1],    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]     # [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

def digitalDifferentialAnalyzer(angle, x0, y0, max_distance = 10):
    """
    Cette fonction permet de retourner les coordonnées du point d'impact avec un obstacle 
    d'un rayon émis depuis la position (x0,y0) d'un joueur avec un angle spécifié en radians.
    - max-distance correspond à la distance maximale de recherhe d'obstacle, 
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
        
        if 0 <= x_cellule <= map.shape[1] and 0 <= y_cellule <= map.shape[0] :
            if map[y_cellule][x_cellule] == 1:

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

def get_rays(window, player, wall_color) :
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
          wall_design = Wall.create(wall_color,"#",counter_x, increment_width)
          draw3DWall(window, res[2], Player.get_angle(player), angle_acc, wall_design)

        angle_acc -= INCREMENT_RAD
        counter_x = round(i * increment_width)

def endGame(window, death, color):

  x_start = P_win.get_width(window) // 16
  y_start = P_win.get_height(window) // 30

  skull = Image.upload_classic_image('images/skull.txt', x_start, y_start, color)
  Image.set_color(skull,Color.create_color(255,0,255))
  Image.draw(window, skull)

  if death == 0:
    text_walls = Image.upload_classic_image('text/walls.txt', int(P_win.get_width(window)*0.48), int(P_win.get_height(window)*0.24), color)
    Image.draw(window, text_walls)

  P_win.get_stdscr(window).refresh()
  time.sleep(10)

def run(stdscr):
  curses.curs_set(0) #Masquer le curseur

  window = P_win.create(stdscr)
  P_win.get_stdscr(window).nodelay(0) #Bloquer/Débloquer l'entrée utilisateur
  P_win.get_stdscr(window).timeout(100) #Faire varier le rafraichissement du terminal en ms 

  # Démarrage du gestionnaire de couleurs :
  curses.start_color()
  green_matrix = Color.create_color(0, 233, 2)

  game_run = Game.create(0.01,map)
  player_run = Player.create([14.5, 9.25], 80)

  NPC.upload_NPC_to_game(game_run, "images/NPCS/chuck.txt")

  while True :

    P_win.refresh_size(window)

    if map[int(Player.get_position(player_run)[1])][int(Player.get_position(player_run)[0])] :
      P_win.get_stdscr(window).clear()
      P_win.get_stdscr(window).refresh()
      endGame(window, 0, green_matrix)
      break

    Player.move(player_run,Game.get_diff_time(game_run),window)
    drawFloor(window)
    get_rays(window, player_run, green_matrix)
    Game.draw_NPC(window,game_run,player_run)

    Game.running_time(game_run)
    time.sleep(Game.get_diff_time(game_run)) # Faire varier le rafraichissment des animations
    
curses.wrapper(run)