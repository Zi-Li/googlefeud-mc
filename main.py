# Python program to create a simple GUI
# Simple Quiz using Tkinter
 
#import everything from tkinter
from tkinter import *
from guistuff import *

if __name__ == '__main__':

    # setup tk
    gui = Tk()
    gui.title("Google Feud")
    fs = FS_Handler(gui)
    
    frontpage(gui)

    gui.mainloop()
