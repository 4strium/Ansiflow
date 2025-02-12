import matplotlib.pyplot as plt
import numpy as np

# Exemple de carte (map)
map = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1],
    [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,1],
    [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1],
    [1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
])

pos = (5.5, 3.5)

# def get_rays(pos_cam):

# Affichage avec une colormap 'gray'
plt.imshow(map, cmap='gray_r', interpolation='nearest', origin='lower', extent=[0, map.shape[1], 0, map.shape[0]])

# Réglage des ticks sur les axes
plt.xticks(np.arange(0, map.shape[1]+1, 1))
plt.yticks(np.arange(0, map.shape[0]+1, 1))

# Affichage de la grille
plt.grid(which='both')

# Ajout du point rouge
plt.plot(pos[0], pos[1], 'ro')

# Affichage du graphique
plt.show()
