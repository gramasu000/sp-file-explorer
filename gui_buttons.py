"""Module: gui_buttons

This module defines wrapper classes for each button widget in our file explorer.
Each wrapper class has the visual characteristics of the widget as its properties.
"""
from tkinter import Button, LEFT, RIGHT, X

class UpButton:
    """UpButton class

    This class is a wrapper to the 'Move Up' button widget
    This button will move the file explorer up one directory
    """

    def _init_settings(self):
        self.text = "Move Up"
        # Height, Width is given in characters
        self.width = 9
        self.height = 1
        self.padx = 4
        self.pady = 4
        self.pack_side = LEFT
        self.pack_fill = X

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Button(parent)
        self.widget.configure(
            text=self.text,
            width=self.width,
            height=self.height,
            padx=self.padx,
            pady=self.pady
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill
        )


class DownButton:
    """DownButton class

    This class is a wrapper to the 'Move Down' button widget
    This button will move the file explorer down a selected directory
    """

    def _init_settings(self):
        self.text = "Move Down"
        self.width = 9
        self.height = 1
        self.padx = 4
        self.pady = 4
        self.pack_side = LEFT
        self.pack_fill = X

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Button(parent)
        self.widget.configure(
            text=self.text,
            width=self.width,
            height=self.height,
            padx=self.padx,
            pady=self.pady
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill
        )


class CloseButton:
    """CloseButton class

    This class is a wrapper to the 'Close' button widget
    This button closes the GUI
    """

    def _init_settings(self):
        self.text = "Close"
        self.width = 9
        self.height = 1
        self.padx = 4
        self.pady = 4
        self.pack_side = RIGHT
        self.pack_fill = X

    def __init__(self, root, parent):
        self._init_settings()
        self.root = root
        self.parent = parent
        self.widget = Button(parent)
        self.widget.configure(
            text=self.text,
            width=self.width,
            height=self.height,
            padx=self.padx,
            pady=self.pady
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill
        )
