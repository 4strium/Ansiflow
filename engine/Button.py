import type.game.Player_Window as P_win

class Button : pass

def create(content, position, color1, color2):
  button_export = Button()

  button_export.content = content
  button_export.position = position
  button_export.color1 = color1
  button_export.color2 = color2

  return button_export

def get_content(button_inp) :
  return button_inp.content
def get_position(button_inp):
  return button_inp.position
def get_color1(button_inp):
  return button_inp.color1
def get_color2(button_inp):
  return button_inp.color2

def set_content(button_inp, n_content):
  button_inp.content = n_content
def set_position(button_inp, n_position):
  button_inp.position = n_position
def set_color1(button_inp, n_color1):
  button_inp.color1 = n_color1
def set_color2(button_inp, n_color2):
  button_inp.color2 = n_color2

def draw_button(window_inp, button_inp, hover):
  if hover :
    color_drawing = get_color2(button_inp)
  else :
    color_drawing = get_color1(button_inp)
  space_needed = len(get_content(button_inp))
  x_fix = get_position(button_inp)[0]
  y_fix = get_position(button_inp)[1]
  x_index = x_fix+1
  P_win.get_stdscr(window_inp).addstr(y_fix+2, x_fix+1,get_content(button_inp), color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix, x_fix,'┌', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+1, x_fix,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+2, x_fix,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+3, x_fix,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+4, x_fix,'└', color_drawing)
  for i in range(space_needed):
    P_win.get_stdscr(window_inp).addstr(y_fix, x_index,'─', color_drawing)
    P_win.get_stdscr(window_inp).addstr(y_fix+4, x_index,'─', color_drawing)
    x_index += 1
  P_win.get_stdscr(window_inp).addstr(y_fix, x_index,'┐', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+1, x_index,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+2, x_index,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+3, x_index,'│', color_drawing)
  P_win.get_stdscr(window_inp).addstr(y_fix+4, x_index,'┘', color_drawing)