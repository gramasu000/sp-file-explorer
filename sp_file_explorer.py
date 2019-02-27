"""Module: sp_file_explorer

This module defines wrapper classes for each widget in our file explorer
It also contains a wrapper class for the entire GUI itself.
"""
from tkinter import Tk

from gui_frames import MainFrame, FileListFrame, ButtonsFrame, ScrollListFrame
from gui_buttons import UpButton, DownButton, CloseButton
from gui_scroll_list_labels import DirectoryLabel, FileScrollListBox

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
        self.up_button = UpButton(self.buttons_frame.widget)
        self.down_button = DownButton(self.buttons_frame.widget)
        self.close_button = CloseButton(self.root, self.buttons_frame.widget)
        self.dir_label = DirectoryLabel(self.flist_frame.widget)
        self.scroll_list_frame = ScrollListFrame(self.flist_frame.widget)
        self.fscroll_list = FileScrollListBox(self.scroll_list_frame.widget) 

if __name__ == "__main__":
    ROOT = Tk()
    GUI = FileExplorerGUI(ROOT)
    ROOT.mainloop()
