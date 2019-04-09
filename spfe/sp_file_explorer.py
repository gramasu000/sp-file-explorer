"""Main module for the simple python file explorer

This module defines the FileExplorer GUI class, whose instance contains 
a basic file explorer application using tkinter.
"""

from os import getcwd, listdir, sep
from os.path import dirname, isdir
from tkinter import StringVar, Frame, Button, Label, Listbox, Scrollbar, W, E, N, S, LEFT, RIGHT, BOTH, SINGLE, VERTICAL, YES

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
        for i in range(5):
            self.root.columnconfigure(i, pad=5, weight=1)
        self.root.rowconfigure(0, weight=1)        
        self.root.rowconfigure(1, weight=1000)        
        self.root.rowconfigure(2, pad=5, weight=1)        

        self.up_button = Button(self.root, text="Move Up", width=9, height=1)
        self.up_button.grid(row=2, column=0)
        
        self.down_button = Button(self.root, text="Move Down", width=9, height=1)
        self.down_button.grid(row=2, column=1)

        self.cut_button = Button(self.root, text="Cut", width=9, height=1)
        self.cut_button.grid(row=2, column=2)

        self.copy_button = Button(self.root, text="Copy", width=9, height=1)
        self.copy_button.grid(row=2, column=3)
 
        self.paste_button = Button(self.root, text="Paste", width=9, height=1)
        self.paste_button.grid(row=2, column=4)
    
        self.dir_label = Label(self.root, height=1, background="white")
        self.dir_label.grid(row=0, columnspan=5, sticky=W+E)

        self.scroll_list_frame = Frame(self.root)
        self.scroll_list_frame.grid(row=1, columnspan=5, sticky=N+S+W+E)

        self.f_listbox = Listbox(self.scroll_list_frame, background="white", activestyle="dotbox", selectmode=SINGLE)
        self.f_listbox.pack(side=LEFT, fill=BOTH, expand=YES) 
         
        self.f_scrollbar = Scrollbar(self.scroll_list_frame, orient=VERTICAL)
        self.f_scrollbar.pack(side=RIGHT, fill=BOTH) 
        
        self.f_listbox.configure(yscrollcommand=self.f_scrollbar.set)
        self.f_scrollbar["command"] = self.f_listbox.yview
        self.logger.info("graphical widgets initialized")

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
        self.logger.info(f"set current directory to {self.curdir}")
        self.dir_label.configure(text=self.curdir)
        self.pardir = dirname(arg_dir)
        self.flist = listdir(arg_dir)
        flist_stringvar = StringVar(self.scroll_list_frame, listdir(arg_dir))
        self.f_listbox.configure(listvariable=flist_stringvar)
        self.f_listbox.yview_moveto(0)
        num_children = len(self.flist)
        if num_children != 1:
            self.logger.info(f"current directory has {num_children} children files")
        else:
            self.logger.info(f"current directory has {num_children} child file") 
        if num_children != 0:
            self.f_listbox.selection_clear(0, len(self.flist) - 1)
            self.f_listbox.selection_set(0)

    def up_callback(self):
        """Event Handler for click of 'Move Up' button

        The text label shows the path to the current directory,
        while the listbox shows all the children of that directory.
        This method sets the new current directory to the parent directory
        and updates the text label and listbox accordingly. 
        """
        self.logger.info("'Move Up' button clicked")
        self._update_dir_info(self.pardir)

    def down_callback(self):
        """Event Handler for click of 'Move Down' button

        The text label shows the path to the current directory,
        while the listbox shows all the children of that directory.
        This method sets the new current directory to a child directory 
        (if a child exists and is a directory) and updates the text label 
        and listbox accordingly.  
        """
        self.logger.info("'Move Down' button clicked")
        if len(self.f_listbox.curselection()) != 0:
            index = self.f_listbox.curselection()[0]
            file_name = self.flist[index]
            file_path = self.curdir + sep + file_name
            if isdir(file_path):
                self._update_dir_info(file_path)
            else:
                self.logger.warn("'Move Down' callback invalid, child file is not a directory")
        else:
            self.logger.warn("'Move Down' callback invalid, no child file was selected")

    def _set_button_callbacks(self):
        """Sets event handlers for the three buttons"""
        self.up_button.configure(command=self.up_callback)
        self.down_button.configure(command=self.down_callback)


    def __init__(self, root, logger):
        """Initializes the sp_file_explorer

        Sets the root, window manager settings.
        Initializes the widgets.
        Sets the button callbacks.
        Sets default contents of text label and listbox 
        (current directory filepath and children respectively)

        Args:
            root (tkinter.Tk) - A Tk gui object which is the 
                                root for the tkinter app.
            logger (logging.Logger) - A Logger object used for 
                                        logging events.
        """
        self.root = root
        self.logger = logger
        self.logger.info("initializing application")
        self._init_window_manager_settings()
        self._init_tk_widgets()
        self._update_dir_info(getcwd())
        self._set_button_callbacks()
