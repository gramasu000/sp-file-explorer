"""Main module for the simple python file explorer

This module defines the FileExplorer GUI class, whose instance contains 
a basic file explorer application using tkinter.
"""

from tkinter import Tk, StringVar, MOVETO
from os import getcwd, listdir, sep
from os.path import dirname, isdir

from .widget_data import MAIN_FRAME_DATA, FILELIST_FRAME_DATA, BUTTONS_FRAME_DATA,\
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
    """A class whose instance contains a basic file explorer application using tkinter

    This class contains all the widgets and event handlers needed for sp_file_explorer.
    The main widgets of this app are the three buttons, the scrollable listbox and the text label.
    The main event handlers are triggered by the buttons and change the scrollable listbox.
    """

    def _init_window_manager_settings(self):
        """Sets any root-level configuration of tkinter gui

        Specifically, we set the title of the gui window
        """
        self.root.wm_title("Simple Python File Explorer")

    def _init_tk_widgets(self):
        """Initialize the widgets of the sp_file_explorer

        We initialize all frames, buttons, label, listbox and scrollbar in the 
        application, and then link the listbox and the scrollbar.
        """
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
        """Update the text label and listbox contents according to arg_dir

        The text label shows the path to the current directory,
        while the listbox shows all the children of that directory.
        This function changes the contents of both widgets 
        to correspond to a new current directory.

        Args:
            arg_dir (str): The filepath of the new current directory 
        """
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

    def up_callback(self):
        """Event Handler for click of 'Move Up' button

        The text label shows the path to the current directory,
        while the listbox shows all the children of that directory.
        This method sets the new current directory to the parent directory
        and updates the text label and listbox accordingly. 
        """
        self._update_dir_info(self.pardir)

    def down_callback(self):
        """Event Handler for click of 'Move Down' button

        The text label shows the path to the current directory,
        while the listbox shows all the children of that directory.
        This method sets the new current directory to a child directory 
        (if a child exists and is a directory) and updates the text label 
        and listbox accordingly.  
        """
        if len(self.f_listbox.curselection()) is not 0:
            index = self.f_listbox.curselection()[0]
            file_name = self.flist[index]
            file_path = self.curdir + sep + file_name
            if isdir(file_path):
                self._update_dir_info(file_path)

    def close_callback(self):
        """Event Handler for click of 'Close' button

        This method destroys all of the widgets in the application
        """
        self.root.destroy()

    def _set_button_callbacks(self):
        """Sets event handlers for the three buttons"""
        self.up_button.configure(command=self.up_callback)
        self.down_button.configure(command=self.down_callback)
        self.close_button.configure(command=self.close_callback)


    def __init__(self, root):
        """Initializes the sp_file_explorer

        Sets the root, window manager settings.
        Initializes the widgets.
        Sets the button callbacks.
        Sets default contents of text label and listbox 
        (current directory filepath and children respectively)

        Args:
            root (tkinter.Tk) - A Tk gui object which is the 
                                root for the tkinter app.   
        """
        self.root = root
        self._init_window_manager_settings()
        self._init_tk_widgets()
        self._update_dir_info(getcwd())
        self._set_button_callbacks()
