#!/usr/bin/env python

from tkinter import Tk

from sp_file_explorer import FileExplorerGUI

if __name__ == "__main__":
    ROOT = Tk()
    GUI = FileExplorerGUI(ROOT)
    ROOT.mainloop()
