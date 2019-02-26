"""Module: gui_scroll_list_labels.py

This module defines wrapper classes for each Label/ListBox/Scrollbar widget in our file explorer.
Each wrapper class has the visual attributes of the widget as properties.
"""
from tkinter import Label, TOP, BOTH

class DirectoryLabel:
    """DirectoryLabel class

    This class is a wrapper to the present-working-directory label widget
    """

    def _init_settings(self):
        self.background = "yellow"
        self.padx = 0
        self.pady = 0
        self.width = 90
        self.height = 1
        self.text = "/home/gautam/Documents/GitRepos/sp-file-explorer/"
        self.pack_side = TOP
        self.pack_fill = BOTH

    def __init__(self, parent):
        self._init_settings()
        self.parent = parent
        self.widget = Label(parent)
        self.widget.configure(
            background=self.background,
            padx=self.padx,
            pady=self.pady,
            width=self.width,
            height=self.height,
            text=self.text
        )
        self.widget.pack(
            side=self.pack_side,
            fill=self.pack_fill
        )
