import subprocess

subprocess.run(["gnome-terminal", "--zoom=0.65", "--full-screen", "--", "bash", "-c", "python3 game_curses_version.py && exec bash"])
