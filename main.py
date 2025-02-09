import subprocess

subprocess.run(["gnome-terminal", "--zoom=0.65", "--", "bash", "-c", "python3 sample.py && exec bash"])
