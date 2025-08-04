from modules.otherTools import checkOS
import subprocess

class ExternalTerminal :
  def __init__(self):
    self.operating_system = checkOS()

  def runGame(self, command=None):
    if self.operating_system == "Windows" :
      if command:
        escaped_command = command.replace('"', '""').replace("'", "''")
        subprocess.run([
          "powershell", 
          "-Command", 
          f"Start-Process powershell -ArgumentList '-NoExit', '-Command', \"{escaped_command}\" -WindowStyle Maximized"
        ])
      else:
        subprocess.run([
          "powershell", 
          "-Command", 
          "Start-Process powershell -WindowStyle Maximized"
        ])
          
    elif self.operating_system == "UNIX" :
      try:
        if subprocess.run(["which", "gnome-terminal"], capture_output=True).returncode == 0:
          if command:
            subprocess.run(["gnome-terminal", "--maximize", "--", "bash", "-c", f"{command}; exec bash"])
          else:
            subprocess.run(["gnome-terminal", "--maximize"])
            
        elif subprocess.run(["which", "konsole"], capture_output=True).returncode == 0:
          if command:
            subprocess.run(["konsole", "--fullscreen", "-e", "bash", "-c", f"{command}; exec bash"])
          else:
            subprocess.run(["konsole", "--fullscreen"])
            
        elif subprocess.run(["which", "xterm"], capture_output=True).returncode == 0:
          if command:
            subprocess.run(["xterm", "-maximized", "-e", f"bash -c '{command}; exec bash'"])
          else:
            subprocess.run(["xterm", "-maximized"])
            
        elif subprocess.run(["which", "osascript"], capture_output=True).returncode == 0:
          if command:
            subprocess.run([
              "osascript", "-e", 
              f'tell application "Terminal" to do script "{command}" activate'
            ])
          else:
            subprocess.run([
              "osascript", "-e", 
              'tell application "Terminal" to do script "" activate'
            ])
        else:
          print("Erreur")
      except Exception :
        print("Erreur")
    else :
      print("Erreur")

if __name__ == "__main__" :
  term = ExternalTerminal()
  term.runGame("python main_engine.py")