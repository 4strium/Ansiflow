import curses
import type.game.Player_Window as P_win
import engine.Color as Color

class Image : pass

def create(path, x, y, color):
  global color_index

  img = Image()

  try :
    with open(path, 'r', encoding='utf-8') as file_txt:
      tmp = file_txt.readlines()
      img.visual = [line.rstrip('\n') for line in tmp]
  except FileNotFoundError :
    return
  
  img.position = []
  img.position.append(x)
  img.position.append(y)

  img.color = color

  return img

def get_visual(img_inp):
  return img_inp.visual
def get_pos(img_inp):
  return img_inp.position
def get_color(img_inp):
  return img_inp.color

def set_pos(img_inp, n_pos):
  img_inp.position = n_pos
def set_color(img_inp, n_color):
  img_inp.color = n_color

def draw(window, img_inp):
  for i in range(len(get_visual(img_inp))) :
    if 0 <= i < P_win.get_height(window) - 1 :
      P_win.get_stdscr(window).addstr(i+img_inp.position[1], img_inp.position[0], img_inp.visual[i], img_inp.color)