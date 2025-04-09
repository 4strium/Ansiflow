import curses
color_index = 1

def create_color(R, G, B):
  global color_index

  color_index += 1
  curses.init_color(color_index, int(R * 1000 / 255), int(G * 1000 / 255), int(B * 1000 / 255))
  curses.init_pair(color_index, color_index, curses.COLOR_BLACK)

  return curses.color_pair(color_index)