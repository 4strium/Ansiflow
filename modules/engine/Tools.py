import curses

def convert_sec_to_min(sec_time):
  """
  Convertit un temps en secondes en (minutes, secondes).
  Ex : 125 -> (2, 5)
  """
  minutes = int(sec_time // 60)
  seconds = int(sec_time % 60)
  return (minutes, seconds)

def get_key(stdscr):
  """
    Capture une touche pressée en utilisant curses.
    Retourne le code de la touche ou None si aucune touche n'est pressée.
    """
  try:
      curses.noecho()
      curses.cbreak()
      stdscr.nodelay(True) 
      
      key = stdscr.getch()
      
      curses.nocbreak()
      curses.echo()
      curses.endwin()
      
      return key if key != -1 else None
      
  except Exception:
      try:
          curses.endwin()
      except:
          pass
      return None
