"""Module: sp_file_explorer

This module defines wrapper classes for each widget in our file explorer
It also contains a wrapper class for the entire GUI itself.
"""
from tkinter import Tk, StringVar
from os import getcwd, listdir, sep
from os.path import dirname, isdir

from gui_frames import MainFrame, FileListFrame, ButtonsFrame, ScrollListFrame
from gui_buttons import UpButton, DownButton, CloseButton
from gui_scroll_list_labels import DirectoryLabel, FileScrollListBox

class FileExplorerGUI:
    """FileExplorerGUI class

    This class is a wrapper to the whole GUI and all its components.
    """

    def _init_visual_settings(self):
        self.width = 800
        self.height = 600
        self.root.geometry(
            "{}x{}".format(self.width, self.height)
        )
        self.root.wm_title("Simple Python File Explorer")
    
    def _init_widgets(self):
        self.main_frame = MainFrame(self.root)
        self.flist_frame = FileListFrame(self.main_frame.widget)
        self.buttons_frame = ButtonsFrame(self.main_frame.widget)
        self.up_button = UpButton(self.buttons_frame.widget)
        self.down_button = DownButton(self.buttons_frame.widget)
        self.close_button = CloseButton(self.root, self.buttons_frame.widget)
        self.dir_label = DirectoryLabel(self.flist_frame.widget)
        self.scroll_list_frame = ScrollListFrame(self.flist_frame.widget)
        self.fscroll_list = FileScrollListBox(self.scroll_list_frame.widget) 

    def _update_dir_info(self, dir):
        self.curdir = dir
        self.dir_label.widget.configure(text=self.curdir)
        self.pardir = dirname(dir)
        self.flist = listdir(dir)
        flist_stringvar = StringVar(self.scroll_list_frame.widget, listdir(dir))
        self.fscroll_list.listbox.configure(listvariable=flist_stringvar)
        if len(self.flist) is not 0:
            self.fscroll_list.listbox.selection_clear(0, len(self.flist) - 1)
            self.fscroll_list.listbox.selection_set(0)

    def _up_callback(self):
        self._update_dir_info(self.pardir)

    def _down_callback(self):
        if len(self.fscroll_list.listbox.curselection()) is not 0:
            index = self.fscroll_list.listbox.curselection()[0]
            file_name = self.flist[index]
            file_path = self.curdir + sep + file_name
            if isdir(file_path):
                self._update_dir_info(file_path)

    def _close_callback(self):
        self.root.destroy()

    def _set_button_callbacks(self):
        self.up_button.widget.configure(command=self._up_callback)
        self.down_button.widget.configure(command=self._down_callback)
        self.close_button.widget.configure(command=self._close_callback)


    def __init__(self, root):
        self.root = root
        self._init_visual_settings()
        self._init_widgets()
        self._update_dir_info(getcwd())
        self._set_button_callbacks()

if __name__ == "__main__":
    ROOT = Tk()
    GUI = FileExplorerGUI(ROOT)
    ROOT.mainloop()
