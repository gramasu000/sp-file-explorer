"""Module: sp_file_explorer

This module defines wrapper classes for each widget in our file explorer
It also contains a wrapper class for the entire GUI itself.
"""

from tkinter import Tk, Frame, TOP, BOTH

class MainFrame:
    """MainFrame class

    This class is a wrapper to the TKinter frame widget
        that will cover the entire GUI
    It will parent the FileListFrame and ButtonsFrame widgets
    """

    def _init_settings(self):
        self.width = 800
        self.height = 600
        self.background = "green"
        self.pack_side = TOP
        self.pack_fill = BOTH

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Frame(self.parent)
        self.widget.configure(
            background=self.background,
            width=self.width,
            height=self.height
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill
        )


class FileListFrame:
    """FileListFrame class

    This class is a wrapper to the TKinter frame widget
        that will hold the widgets showing the list of files in a directory.
    """

    def _init_settings(self):
        self.width = 790
        self.height = 550
        self.background = "white"
        self.borderwidth = 3
        self.relief = "ridge"
        self.pack_side = TOP
        self.pack_fill = BOTH
        self.pack_padx = 5
        self.pack_pady = 5

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Frame(self.parent)
        self.widget.configure(
            background=self.background,
            width=self.width,
            height=self.height,
            borderwidth=self.borderwidth,
            relief=self.relief
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill,
            padx=self.pack_padx,
            pady=self.pack_pady
        )


class ButtonsFrame:
    """ButtonsFrame class

    This class is a wrapper to the TKinter frame widget
        that will hold all the buttons of the app.
    It will parent the UpButton, DownButton and CloseButton classes
    """

    def _init_settings(self):
        self.width = 790
        self.height = 35
        self.background = "orange"
        self.pack_side = TOP
        self.pack_fill = BOTH
        self.pack_padx = 5
        self.pack_pady = 5

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Frame(self.parent)
        self.widget.configure(
            background=self.background,
            width=self.width,
            height=self.height
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill,
            padx=self.pack_padx,
            pady=self.pack_pady
        )


class FileExplorerGUI:
    """FileExplorerGUI class

    This class is a wrapper to the whole GUI and all its components.
    """

    def _init_settings(self):
        self.width = 800
        self.height = 600
        self.root.geometry(
            "{}x{}".format(self.width, self.height)
        )
        self.root.wm_title("Simple Python File Explorer")

    def __init__(self, root):
        self.root = root
        self._init_settings()
        self.main_frame = MainFrame(self.root)
        self.flist_frame = FileListFrame(self.main_frame.widget)
        self.buttons_frame = ButtonsFrame(self.main_frame.widget)


if __name__ == "__main__":
    ROOT = Tk()
    GUI = FileExplorerGUI(ROOT)
    ROOT.mainloop()
