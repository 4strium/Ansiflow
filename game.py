import matplotlib.pyplot as plt
import numpy as np
import math

PI = 3.142 # Je fixe pi à une certaine valeur pour éviter des problèmes liés à l'approximation des flottants

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




def demi_droite_points(x, y, alpha, step=0.001):
    points = []
    cos_a, sin_a = math.cos(alpha), math.sin(alpha)
    
    t = 0
    while t < map.shape[1]:
        x_new = x + t * cos_a
        y_new = y + t * sin_a

        if abs(x_new - round(x_new)) < 1e-3 :
            arrondi_float = round(y_new, 3)
            if abs(int(arrondi_float) - arrondi_float) < 1e-2 :
                arrondi_float = int(arrondi_float)
            elif abs(int(arrondi_float+1) - arrondi_float) < 1e-2 :
                arrondi_float = int(arrondi_float) +1
            points.append((round(x_new), arrondi_float))
        if abs(y_new - round(y_new)) < 1e-3 :
            arrondi_float = round(x_new, 3)
            if abs(int(arrondi_float) - arrondi_float) < 1e-2 :
                arrondi_float = int(arrondi_float)
            elif abs(int(arrondi_float+1) - arrondi_float) < 1e-2 :
                arrondi_float = int(arrondi_float) +1
            points.append((arrondi_float, round(y_new)))
        t += step
    
    points.sort(key=lambda p: math.hypot(p[0] - x, p[1] - y))

    # Supprimer les doublons dû au manque de précision des flottants
    unique_points_x = [x]
    unique_points_y = [y]
    seen = []
    for point in points:
        if point not in seen  :
            unique_points_x.append(point[0])
            unique_points_y.append(point[1])          
            seen.append(point)

    return (unique_points_x, unique_points_y)

def get_rays(position, angle_step, limite) :
    angle_acc = 0


    while angle_acc < limite :
        rayon_out = demi_droite_points(position[0], position[1], angle_acc)

        print(rayon_out)

        for i in range(len(rayon_out[0])-1, 0, -1) :

            index_x = int(rayon_out[0][i])
            print("Index X :",index_x)
            index_y = int(rayon_out[1][i])
            print("Index Y:",index_y,"\n")

            if 0 <= index_y < map.shape[0] and 0 <= index_x < map.shape[1] :
                if map[index_y][index_x] == 1 :

                    plt.plot(index_x, index_y, 'mo')
                    if rayon_out[0] == sorted(rayon_out[0], reverse=True) and angle_acc != PI/2:
                        x_rays = rayon_out[0][:i]
                        print(x_rays)
                        y_rays = rayon_out[1][:i]
                        print(y_rays)
                    elif rayon_out[1] == sorted(rayon_out[1], reverse=True) and rayon_out[0] == sorted(rayon_out[0], reverse=False) and angle_acc != 0:
                        x_rays = rayon_out[0][:i]
                        print(x_rays)
                        y_rays = rayon_out[1][:i]
                        print(y_rays)
                    else:
                        x_rays = rayon_out[0][:i+1]
                        print(x_rays)
                        y_rays = rayon_out[1][:i+1]
                        print(y_rays)

        plt.plot(x_rays, y_rays, linestyle='-', color='lime')


        print('\n\n')
        angle_acc += angle_step


# Affichage avec une colormap 'gray'
plt.imshow(map, cmap='gray_r', interpolation='nearest', origin='lower', extent=[0, map.shape[1], 0, map.shape[0]])

# Réglage des ticks sur les axes
plt.xticks(np.arange(0, map.shape[1]+1, 1))
plt.yticks(np.arange(0, map.shape[0]+1, 1))

# Affichage de la grille
plt.grid(which='both')

# Ajout du point rouge représentant le joueur :
pos = (7.5, 10.5)
plt.plot(pos[0], pos[1], 'ro')

# Ajout des rayons 
get_rays(pos, PI/16, PI*2)

# Affichage du graphique
plt.show()