def convert_sec_to_min(sec_time):
  """
  Convertit un temps en secondes en (minutes, secondes).
  Ex : 125 -> (2, 5)
  """
  minutes = int(sec_time // 60)
  seconds = int(sec_time % 60)
  return (minutes, seconds)

def get_key(stdscr, timeout=0.0):
  """
    Capture une touche pressée en utilisant curses.
  """
  stdscr.timeout(int(timeout * 1000))
  key = stdscr.getch()
  return key
