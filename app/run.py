# Import GUI library
from tkinter import Tk

from desktopapp import DesktopApp

# Initialise desktop frame - 720p
root = Tk()
root.config(background='white')
root.geometry("1280x720")

# Initialise window and networking
app = DesktopApp(root)

# Run GUI in main thread
root.mainloop()
