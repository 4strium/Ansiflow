import termios
import sys
import tty

def get_touch():
    fd = sys.stdin.fileno()
    anciens_parametres = termios.tcgetattr(fd)
    nouvelles_config = termios.tcgetattr(fd)

    # Désactiver l'ECHO (affichage automatique)
    nouvelles_config[3] = nouvelles_config[3] & ~(termios.ECHO | termios.ICANON)

    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, nouvelles_config)
        touche = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, anciens_parametres)
    return ord(touche)