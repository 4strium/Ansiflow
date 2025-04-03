class play_window : pass

def refresh_size(win_inp):
  win_inp.height, win_inp.width = win_inp.stdscr.getmaxyx()

def create(win):
  window = play_window()
  window.stdscr = win
  refresh_size(window)
  return window

def set_stdscr(win_inp, n_stdscr):
  win_inp.stdscr = n_stdscr
def set_height(win_inp, n_height):
  win_inp.height = n_height
def set_width(win_inp, n_width):
  win_inp.width = n_width

def get_stdscr(win_inp): return win_inp.stdscr
def get_height(win_inp): return win_inp.height
def get_width(win_inp): return win_inp.width