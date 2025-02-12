import matplotlib.pyplot as plt
import numpy as np
import math

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
            points.append((round(x_new), round(y_new, 3)))
        if abs(y_new - round(y_new)) < 1e-3 :
            points.append((round(x_new, 3), round(y_new)))
        t += step  # Augmenter par le pas défini


    points.sort(key=lambda p: math.hypot(p[0] - x, p[1] - y))

    # Supprimer les doublons dû au manque de précision des flottants
    unique_points_x = [x]
    unique_points_y = [y]
    seen = set()
    for point in points:
        if point[0] not in seen and point[1] not in seen :
            unique_points_x.append(point[0])
            unique_points_y.append(point[1])          
            if sin_a not in [1, -1] : 
                seen.add(point[0])
            if cos_a not in [1, -1] :
                seen.add(point[1])

    return (unique_points_x, unique_points_y)

def get_rays(position, angle_step, limite) :
    angle_acc = 0


    while angle_acc < limite :
        rayon_out = demi_droite_points(position[0], position[1], angle_acc)

        print(rayon_out)

        for i in range(len(rayon_out[0])-1, 0, -1) :
            index_x = round(rayon_out[0][i])-1
            print(index_x)
            index_y = round(rayon_out[1][i])-1

            if 0 <= index_y < map.shape[0] and 0 <= index_x < map.shape[1] :
                if map[index_y][index_x] == 1 :

                    plt.plot(index_x, index_y, 'mo')
                    if math.pi <= angle_acc < math.pi*2-0.01 :
                        x_rays = rayon_out[0][:i+1]
                        print(x_rays)
                        y_rays = rayon_out[1][:i+1]
                        print(y_rays)
                    else :
                        x_rays = rayon_out[0][:i]
                        print(x_rays)
                        y_rays = rayon_out[1][:i]
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
pos = (5.5, 3.5)
plt.plot(pos[0], pos[1], 'ro')

# Ajout des rayons 
get_rays(pos, math.pi/16, math.pi*2)

# Affichage du graphique
plt.show()