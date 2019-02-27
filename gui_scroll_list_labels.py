"""Module: gui_scroll_list_labels.py

This module defines wrapper classes for each Label/ListBox/Scrollbar widget in our file explorer.
Each wrapper class has the visual attributes of the widget as properties.
"""
from tkinter import Label, Listbox, Scrollbar, TOP, LEFT, RIGHT, BOTH, VERTICAL

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


class FileScrollListBox:
    """FileScrollListBox class

    This class is a wrapper to a listbox of children files and the associated scrollbar 
    """

    def _init_listbox_settings(self):
        self.l_background = "white"
        self.l_width = 770
        self.l_height = 530
        self.l_activestyle = "dotbox"
        self.l_pack_side = LEFT
        self.l_pack_fill = BOTH
        
    def _init_scrollbar_settings(self):
        self.s_pack_side = RIGHT
        self.s_pack_fill = BOTH

    def _init_listbox(self):
        self.listbox = Listbox(self.parent)
        self.listbox.configure(
            background=self.l_background,
            width=self.l_width,
            height=self.l_height,
            activestyle=self.l_activestyle
        )
        self.listbox.pack(
            side=self.l_pack_side,
            fill=self.l_pack_fill
        )

    def _init_scrollbar(self):
        self.scrollbar = Scrollbar(self.parent)
        self.scrollbar.configure(
            orient=VERTICAL
        )
        self.scrollbar.pack(
            side=self.s_pack_side,
            fill=self.s_pack_fill
        )
        
    def __init__(self, parent):
        self.parent = parent
        self._init_listbox_settings()
        self._init_listbox() 
        self._init_scrollbar_settings()
        self._init_scrollbar()
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.listbox.yview
