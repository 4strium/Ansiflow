import numpy as np
import math
import curses
import time

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

GREEN_MATRIX = (0, 233, 2)

# Exemple de carte (map)
map = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],    # [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],    # [1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1]
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],    # [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1]
    [1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1],    # [1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1]
    [1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1],    # [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1]
    [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],    # [1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1]
    [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],    # [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1]
    [1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],    # [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1],    # [1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1]
    [1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1],    # [1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1]
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],    # [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1]
    [1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1],    # [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
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

def draw3DWall(window, ray_distance, player_angle, ray_angle, x_start, increment_width, window_height, window_width) :
  # Correction de l'effet "fish-eye" :
  angle_fix = player_angle - ray_angle
  if angle_fix < 0 :
   angle_fix += 2*PI
  elif angle_fix > 2*PI :
   angle_fix -= 2*PI
  ray_distance = ray_distance * math.cos(angle_fix)

  if ray_distance < 0.1 :
    ray_distance = 0.1

  lineHeight = window_height / ray_distance
  if lineHeight > window_height :
    lineHeight = window_height

  center_h = window_height // 2 
  y_start = center_h - (lineHeight //2)

  end_range = round(x_start + increment_width) +1

  for y_axis in range(round(y_start), round(y_start + lineHeight)) :
    if 0 <= y_axis < window_height-1:
      for i in range(round(x_start), end_range) :
        if 0 <= i < window_width:
          if i == end_range-1 :
            window.addstr(y_axis, i, " ")
          else :
            window.addstr(y_axis, i, "#", curses.color_pair(1))

def drawFloor(window, window_height, window_width) :
  for y_axis in range(window_height//2, window_height) :
    if 0 <= y_axis < window_height -1 :
      for x_axis in range(0, window_width) :
        window.addstr(y_axis, x_axis, "-")

def get_rays(window, angle_init, pos_x, pos_y, window_height, window_width, fov = 80) :
    """
    Procédure qui génére des rayons à partir de la position du joueur (pos_x, pos_y).
    - angle_init : angle en radians situé en plein milieu du champ de vision
    - fov : champ de vision en degrés. p
    Pour la valeur par défaut, 60°, l'algorithme trace donc des rayons de collision sur un angle de 30° à gauche de "angle_init", ainsi que sur 30° à droite de "angle_init".
    """

    angle_acc = angle_init + (fov//2) * INCREMENT_RAD
    increment_width = window_width / fov
    counter_x = 0 

    for i in range(0,fov+1) :
        res = digitalDifferentialAnalyzer(angle_acc, pos_x, pos_y)
        if res != None :
            draw3DWall(window, res[2], angle_init, angle_acc, counter_x, increment_width, window_height, window_width)

        angle_acc -= INCREMENT_RAD
        counter_x = round(i * increment_width)

def main(stdscr):
  curses.curs_set(0) #Masquer le curseur
  stdscr.nodelay(0) #Bloquer/Débloquer l'entrée utilisateur
  stdscr.timeout(100) #Faire varier le rafraichissement du terminal en ms 

  # Démarrage du gestionnaire de couleurs :
  curses.start_color()

  curses.start_color()
  curses.init_color(1, int(GREEN_MATRIX[0] * 1000 / 255), int(GREEN_MATRIX[1] * 1000 / 255), int(GREEN_MATRIX[2] * 1000 / 255))
  curses.init_pair(1, 1, curses.COLOR_BLACK)

  # On fixe la position du joueur :
  pl_position_x = 3.1
  pl_position_y = 9.25

  # On fixe l'angle de perception :
  angle_percep = PI/6

  while True :

    window_height, window_width = stdscr.getmaxyx()

    key = stdscr.getch() 
    
    if key == 27:  # Quitter avec 'échap'
      break
    elif key == ord('z'):
      # Simuler l'avancement du personnage :
      pl_position_x += 0.1 * math.cos(angle_percep)
      pl_position_y += 0.1 * math.sin(angle_percep)
      stdscr.clear()
    elif key == ord('s'):
      # Simuler le reculement du personnage par rapport au sol :
      pl_position_x -= 0.1 * math.cos(angle_percep)
      pl_position_y -= 0.1 * math.sin(angle_percep) 
      stdscr.clear()  
    elif key == ord('q'):
      angle_percep += 0.1
      stdscr.clear()
    elif key == ord('d'):
      angle_percep -= 0.1
      stdscr.clear()

    drawFloor(stdscr, window_height, window_width)
    get_rays(stdscr, angle_percep, pl_position_x, pl_position_y, window_height, window_width)

    time.sleep(0.1) # Faire varier le rafraichissment des animations

        
curses.wrapper(main)