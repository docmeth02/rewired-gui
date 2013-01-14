import Tkinter as tk
from socket import gethostname
from includes import app
import random
from platform import system
from os import devnull
import sys
root = tk.Tk()
rand = random.Random()
try:
    check = sys.frozen
    sys.stdout = open(devnull, 'w')
    sys.stderr = open(devnull, 'w')
except:
    pass
client = app.ThreadedApp(root)
root.mainloop()
