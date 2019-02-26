"""Module: gui_frames

This module defines a wrapper class for each frame widget in our file explorer app
Each wrapper class has the visual attributes of the widget as properties
"""
from tkinter import Frame, TOP, BOTH, BOTTOM

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
    This will parent the UpButton, DownButton and CloseButton classes
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

class ScrollListFrame:
    """ScrollListFrame class

    This class is a wrapper to the TKinter frame widget
        that will hold the scrollable list of files.
    This will parent the FileList and FileScroll widget wrappers
    """

    def _init_settings(self):
        self.width = 790
        self.height = 530
        self.background = "blue"
        self.pack_side = BOTTOM
        self.pack_fill = BOTH
        self.pack_padx = 0
        self.pack_pady = 0

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
