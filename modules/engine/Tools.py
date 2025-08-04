import sys
from modules.otherTools import checkOS

def convert_sec_to_min(sec_time):
  """
  Convertit un temps en secondes en (minutes, secondes).
  Ex : 125 -> (2, 5)
  """
  minutes = int(sec_time // 60)
  seconds = int(sec_time % 60)
  return (minutes, seconds)

if checkOS() == "UNIX" :
  import select, termios, tty
  def init_cbreak():
      """
      Passe stdin en mode cbreak (lecture caractère par caractère sans entrer).
      Retourne les anciens attributs du terminal pour pouvoir les restaurer.
      """
      fd = sys.stdin.fileno()
      old_attrs = termios.tcgetattr(fd)
      tty.setcbreak(fd)
      return old_attrs

  def restore_terminal(old_attrs):
      """
      Restaure les attributs du terminal sauvegardés précédemment.
      """
      termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_attrs)

  def get_key_UNIX(timeout=0.0):
      """
      Lit une touche sans bloquer plus de `timeout` secondes.
      - Si une touche est pressée dans l'intervalle, renvoie son code `ord()`.
      - Sinon, renvoie None.
      """
      fd = sys.stdin.fileno()
      old_attrs = init_cbreak()
      try:
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
          ch = sys.stdin.read(1)
          return ord(ch)
      finally:
          restore_terminal(old_attrs)
      return None
else :
   import msvcrt

def get_key(timeout=0.0):
  """
  Capture une touche pressée de manière non-bloquante, compatible avec tous les systèmes d'exploitation.
  """
  if checkOS() == "Windows" :
    if msvcrt.kbhit():
      return ord(msvcrt.getch().decode('utf-8'))
    return None
  else :
    return get_key_UNIX(timeout)
