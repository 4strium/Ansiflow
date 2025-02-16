import matplotlib.pyplot as plt
import numpy as np
import math

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants.
INCREMENT_RAD = 0.017 # De même, je fixe une valeur arbitraire correspondant à un degré en radian, pour la même raison.

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
        
        if 0 <= x_cellule <= map.shape[0] and 0 <= y_cellule <= map.shape[1] :
            if map[y_cellule][x_cellule] == 1:

                # On calcule les coordonnées exactes du point d'impact en fonction du déplacement du rayon :
                impact_x = x0 + distance * dx
                impact_y = y0 + distance * dy
                
                return (impact_x, impact_y, distance)

    return None


def get_rays(angle_init, pos_x, pos_y, fov = 60) :
    """
    Procédure qui génére des rayons à partir de la position du joueur (pos_x, pos_y).
    - angle_init : angle en radians situé en plein milieu du champ de vision
    - fov : champ de vision en degrés. p
    Pour la valeur par défaut, 60°, l'algorithme trace donc des rayons de collision sur un angle de 30° à gauche de "angle_init", ainsi que sur 30° à droite de "angle_init".
    """

    angle_acc = angle_init + (fov//2) * INCREMENT_RAD

    for i in range(0,fov) :
        res = digitalDifferentialAnalyzer(angle_acc, pos_x, pos_y)
        if res != None :
            plt.plot([pos_x, res[0]], [pos_y, res[1]], "lime")

        angle_acc -= INCREMENT_RAD

# Affichage avec une colormap 'gray'
plt.imshow(map, cmap='gray_r', interpolation='nearest', origin='lower', extent=[0, map.shape[1], 0, map.shape[0]])

# Réglage des ticks sur les axes
plt.xticks(np.arange(0, map.shape[1]+1, 1))
plt.yticks(np.arange(0, map.shape[0]+1, 1))

# Affichage de la grille
plt.grid(which='both')

# On fixe la position du joueur :
pos = (3.1, 9.25)

# On fixe l'angle de perception :
angle_percep = PI/6

get_rays(angle_percep, pos[0], pos[1])

# Ajout du point rouge représentant le joueur :
plt.plot(pos[0], pos[1], 'ro')

# Affichage du graphique
plt.show()