"""Module: sp_file_explorer

This module defines wrapper classes for each widget in our file explorer
It also contains a wrapper class for the entire GUI itself.
"""
from tkinter import Tk, StringVar, MOVETO
from os import getcwd, listdir, sep
from os.path import dirname, isdir

from widget_data import MAIN_FRAME_DATA, FILELIST_FRAME_DATA, BUTTONS_FRAME_DATA,\
    SCROLL_LIST_FRAME_DATA, UP_BUTTON_DATA, DOWN_BUTTON_DATA, CLOSE_BUTTON_DATA,\
    DIRECTORY_LABEL_DATA, FILE_LISTBOX_DATA, FILE_SCROLLBAR_DATA


def make_tk_widget(data, parent):
    """Creates a tkinter.Widget object with given visual/packing data and parent object

    This function instantiates, configures and returns a tkinter gui object
    (i.e. tkinter.Frame, tkinter.Button, tkinter.Listbox)
    aacording to the details in the data argument.

    Args:
        data (dict): A dictionary with "widget_type", "attrs", and "pack_attrs"
                    keys defined.
        parent: A tkinter.Widget object which is the parent of the widget returned   

    Returns:
        tkinter.Widget: A widget in a tkinter application

    Example:
        The following code
    
            widget = tkinter.Frame(parent)
            widget.configure(background="white")
            widget.pack(side=tkinter.TOP)
       
        is equivalent to  
    
            data = { "widget_type": tkinter.Frame, 
                "attrs": { 
                   "background": "white"     
                },
                "pack_attrs": {
                    "side": tkinter.TOP             
                }
            }
            widget = make_tk_widget(data, parent)

        Although it seems that the first code block is shorter,
            the second code block allows us to abstract away
            the visual/packing properties of the widget
            from the instantiation.  
    """
    tk_widget = data["widget_type"](parent)
    tk_widget.configure(**data["attrs"])
    tk_widget.pack(**data["pack_attrs"])
    return tk_widget

class FileExplorerGUI:
    """FileExplorerGUI class

    This class is a wrapper to the whole GUI and all its components.
    """

    def _init_window_manager_settings(self):
        self.root.wm_title("Simple Python File Explorer")

    def _init_tk_widgets(self):
        self.main_frame = make_tk_widget(MAIN_FRAME_DATA, parent=self.root)
        self.flist_frame = make_tk_widget(FILELIST_FRAME_DATA, parent=self.main_frame)
        self.buttons_frame = make_tk_widget(BUTTONS_FRAME_DATA, parent=self.main_frame)
        self.up_button = make_tk_widget(UP_BUTTON_DATA, parent=self.buttons_frame)
        self.down_button = make_tk_widget(DOWN_BUTTON_DATA, parent=self.buttons_frame)
        self.close_button = make_tk_widget(CLOSE_BUTTON_DATA, parent=self.buttons_frame)
        self.dir_label = make_tk_widget(DIRECTORY_LABEL_DATA, parent=self.flist_frame)
        self.scroll_list_frame = make_tk_widget(SCROLL_LIST_FRAME_DATA, parent=self.flist_frame)
        self.f_listbox = make_tk_widget(FILE_LISTBOX_DATA, parent=self.scroll_list_frame)
        self.f_scrollbar = make_tk_widget(FILE_SCROLLBAR_DATA, parent=self.scroll_list_frame)
        self.f_listbox.configure(yscrollcommand=self.f_scrollbar.set)
        self.f_scrollbar["command"] = self.f_listbox.yview

    def _update_dir_info(self, arg_dir):
        self.curdir = arg_dir
        self.dir_label.configure(text=self.curdir)
        self.pardir = dirname(arg_dir)
        self.flist = listdir(arg_dir)
        flist_stringvar = StringVar(self.scroll_list_frame, listdir(arg_dir))
        self.f_listbox.configure(listvariable=flist_stringvar)
        self.f_listbox.yview_moveto(0)
        if len(self.flist) is not 0:
            self.f_listbox.selection_clear(0, len(self.flist) - 1)
            self.f_listbox.selection_set(0)

    def _up_callback(self):
        self._update_dir_info(self.pardir)

    def _down_callback(self):
        if len(self.f_listbox.curselection()) is not 0:
            index = self.f_listbox.curselection()[0]
            file_name = self.flist[index]
            file_path = self.curdir + sep + file_name
            if isdir(file_path):
                self._update_dir_info(file_path)

    def _close_callback(self):
        self.root.destroy()

    def _set_button_callbacks(self):
        self.up_button.configure(command=self._up_callback)
        self.down_button.configure(command=self._down_callback)
        self.close_button.configure(command=self._close_callback)


    def __init__(self, root):
        self.root = root
        self._init_window_manager_settings()
        self._init_tk_widgets()
        self._update_dir_info(getcwd())
        self._set_button_callbacks()

if __name__ == "__main__":
    ROOT = Tk()
    GUI = FileExplorerGUI(ROOT)
    ROOT.mainloop()
