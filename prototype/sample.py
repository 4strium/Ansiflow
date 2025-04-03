import curses
import time
# import random

# Global variables :
dark_spots = "-"
medium_spots = "+"
resolution_texture = 10
longeur_pave = 6


def draw_couloir(win, h, w, pair_pave, pair_index, impair_pave, impair_index):
  x, y = w // 10, h // 7

  start_couloir_y = 2*y
  size_end_couloir_x = 2*x
  size_end_couloir_y = 2*y

  decalage = 0

  for y_axis in range(start_couloir_y):
    for x_axis in range(w):
      if not (decalage <= x_axis <= (w - decalage)):
        win.addstr(y_axis, x_axis, "@", curses.color_pair(1))
    decalage += 6
  
  start_couloir_y = y_axis + 1

  size_end_couloir_x = w-(decalage*2)

  # Milieu de l'image :
  for y_axis in range(size_end_couloir_y):
    for x_axis in range(decalage):
      win.addstr(start_couloir_y + y_axis, x_axis, "@", curses.color_pair(1))
      win.addstr(start_couloir_y + y_axis, (decalage+size_end_couloir_x)+x_axis, "@", curses.color_pair(1))

  y_end_couloir = start_couloir_y + y_axis

  # Sol :
  for y_axis in range(h-y_end_couloir-1):

    # Texturage :
    espace_dispo =  w - (decalage*2)
    calcul_placement = espace_dispo // resolution_texture
    nb_pixels_espacement = (espace_dispo - (calcul_placement*8)) // (resolution_texture+1)

    for x_axis in range(w):    

      for i in range(resolution_texture):
        start_pos = decalage + i * (nb_pixels_espacement + calcul_placement) # On calcule à combien de couples (espacement & briques) on est du bord gauche.

        for j in range(nb_pixels_espacement): # On place les caractères représentant les espacements
          if start_pos + j < w - decalage:
            win.addstr(y_end_couloir + y_axis, start_pos + j, dark_spots)

        for j in range(calcul_placement): # On place les caractères représentant les pavés.
          if (start_pos + nb_pixels_espacement + j < w - decalage) and (((i in pair_index) and ((y_axis % longeur_pave) == pair_pave))or((i in impair_index) and ((y_axis % longeur_pave) == impair_pave))) :
            win.addstr(y_end_couloir + y_axis, start_pos + nb_pixels_espacement + j, dark_spots)
          elif (start_pos + nb_pixels_espacement + j < w - decalage):
            win.addstr(y_end_couloir + y_axis, start_pos + nb_pixels_espacement + j, medium_spots)
      else :
        win.addstr(y_end_couloir + y_axis, x_axis, "@", curses.color_pair(1))
        win.addstr(y_end_couloir + y_axis, w - x_axis - 1, "@", curses.color_pair(1))

    decalage = max(0, decalage - 2)

  win.refresh()

def main(stdscr):
  curses.curs_set(0) #Masquer le curseur
  stdscr.nodelay(0) #Bloquer/Débloquer l'entrée utilisateur
  stdscr.timeout(100) #Faire varier le rafraichissement du terminal en ms 

  # Start color functionality
  curses.start_color()

  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

  pair_pave = longeur_pave//2
  impair_pave = 0
  pair_index = [i for i in range(resolution_texture + 1) if i % 2 == 0]
  impair_index = [j for j in range(resolution_texture +1) if j % 2 == 1]

  while True :

    stdscr.clear()
    height, width = stdscr.getmaxyx()

    draw_couloir(stdscr, height, width, pair_pave, pair_index, impair_pave, impair_index)

    key = stdscr.getch() 
    
    if key == 27:  # Quitter avec 'échap'
        break
    elif key == ord('z'):
      # Simuler l'avancement du personnage par rapport au sol :
      pair_pave = (pair_pave + 1)%longeur_pave
      impair_pave = (impair_pave + 1)%longeur_pave
    elif key == ord('s'):
      # Simuler le reculement du personnage par rapport au sol :
      pair_pave = (pair_pave - 1)%longeur_pave
      impair_pave = (impair_pave - 1)%longeur_pave    

    time.sleep(0.01) # Faire varier le rafraichissment des animations

curses.wrapper(main)