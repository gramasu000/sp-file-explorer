"""Simple Python File Explorer

Simple Python File Explorer is a GUI program written using the Tkinter module
    from Python's Standard Library.
This module, sp_file_explorer, defines all of the classes and functions necessary 
    to run the application.

This program uses a Redux-like approach to managing the state of the application.
Refer to https://redux.js.org/introduction/core-concepts for more information.

The state of the application is a python dictionary, with the following keys.
    
    state = {
        "directory": (str - Directory the application is viewing),
        "children": (list - List of filenames who are children of the directory above),
        "selected": (list - A subset of the list of children - denotes those which are selected),
        "scroll_data": {
            "list_size": (int - height (number of lines) of the visible list widget),
            "list_width": (int - width (number of characters) of the visible list widget),
            "scroll_trigger": (int - if you select a file within this margin from the top or bottom of list, the list will scroll),
            "scroll_top": (int - file index (in children list) of top line of listbox; indicates vertical scroll position), 
        },
        "mode": (str - Enumeration of 'mode' of application; valid values are ['browse', 'command','quit'])
        "prompt_data": {
            "cmd_prompt": (str - String to show when application is in command mode)
            "brs_prompt": (str - String to show when application is in browse mode)
        }
        "text": (str - Contents of text widget, displayed in the application) 
    }

This dictionary is a single source of truth for the state of the application, and is never modified directly.
If the user wants to change the state, they do so by using reducers.
Reducers are functions which take in a state (plus other data) and outputs out a new state which represents
    the change the user is seeking.

The first and formost class to mention is the Application class. 
This class holds all of the Tkinter widgets of the GUI, and binds callback functions to events.
It also has a state property to hold the python dictionary matching the current application state.

There are two classes which hold reducer functions - BasicReducer and KeyBindReducer.
BasicReducer and KeyBindReducer hold reducers as class methods.
BasicReducer hold reducers which make (relatively) straightforward changes to the state
In contrast, KeyBindReducer hold reducers which make more complicated changes to the state, 
    many times depending on the previous state itself (resulting in many if-else statements).
KeyBindReducer methods always call either one BasicReducer method or a composition of BasicReducer methods,
    and are used directly as part of callback functions for application events.

The Renderer class holds a class method called render.
Renderer.render takes in state dictionary and an Application instance
    and changes widget properties for the application to match the state.
In other words, it "renders" the application to match the state.

Finally, since this is a file explorer application, the app uses the python os library heavily.
The FileSystem class holds class methods to abstract away calls to the os library.

The module also has a global object LOGGER, which is the module level logger.

To run this application, run it just as you would run a python script.

    $ python sp_file_explorer.py

"""

import sys
import os
import copy
import logging
from tkinter import Tk, Label, Listbox, Scrollbar, Text, N, S, E, W, VERTICAL, END, DISABLED, NORMAL, NONE, INSERT, DISABLED, StringVar


def initLogging(logger_name, logfile_name):
    """Initializes a object for logging 

    This function returns a logging.Logger object which has two handlers 
        - a stream handler to output to console 
        - a file handler to output to file
    The stream handler will handle log records of level INFO and above
    The file handler will handle log records of level DEBUG and above
    
    Args:
        logger_name (str): Name of logging.Logger object
        logfile_name (str): Name of log file
    
    Returns:  
        logging.Logger: logger object to use for application
    """
    logger = logging.getLogger(logger_name)
    if len(logger.handlers) == 0 and logger.getEffectiveLevel() == logging.WARN:
        formatter = logging.Formatter(style="{", fmt="({name}) {asctime}-{levelname}: {message}")
        handler1 = logging.StreamHandler()
        handler1.setLevel(logging.INFO)
        handler1.setFormatter(formatter)
        handler2 = logging.FileHandler(logfile_name)
        handler2.setLevel(logging.DEBUG)
        handler2.setFormatter(formatter)
        logger.addHandler(handler1)
        logger.addHandler(handler2)
        logger.setLevel(logging.DEBUG)
    return logger


LOGGER = initLogging(__name__, "sp_file_explorer.log")
"""logging.Logger: Module Level Logger 

This global logger can be called by any function of any class in the module.
"""

class FileSystem:
    """Class holding static methods for file system functions

    This class has static methods which use functions from python os library.
    Thus, it provides a separation between file system functions and the rest of the application.
    It also allows us (developers) to construct file system functions of arbitrary complexity as needed
        by just adding a static method to this class.  
    """
    
    @staticmethod
    def currentDir():
        """ Returns the current working directory 

        Returns:
            str: The current working directory 
        """
        return os.getcwd()

    @staticmethod
    def listDir(dir):
        """ Returns the list of children files of  directory 
    
        Args:
            dir (str): A directory filepath
    
        Returns:
            list: List of children filenames of 'dir'
        """
        return os.listdir(dir)

    @staticmethod
    def parent(path):
        """ Given a file's filepath, returns the parent directory

        Args:
            path (str): Filepath of a file

        Returns:
            str: Filepath of the parent directory of file 
        """ 
        return os.path.dirname(path)

    @staticmethod
    def pathOfChild(dir, child):
        """ Given a filename and parent directory path, return the file's path

        Args:
            dir (str): Filepath of parent directory
            child (str): Filename of child file

        Returns:
            str: Filepath of child file 
        """
        return os.path.join(dir, child)

    @staticmethod
    def isChildOpenable(path):
        """ Given a path, returns a boolean indicating if the file is 'openable'

        Args:
            path (str): Filepath of a file

        Returns:
            bool: True if file is a directory with appropriate permissions, False otherwise

        Todo:
            Right now, this function only checks if file is a directory.
            Also include if the user has permissions to open the file.
        """
        return os.path.isdir(path)   

    @staticmethod
    def dirOrFile(path):
        """ Given a path, returns a str indicating if the path is a file or directory

        Args:
            path (str): Filepath of a file

        Returns:
            str: 'dir' if file is a directory with appropriate permissions, 'file' otherwise
        """
        if os.path.isdir(path):
            return "dir"
        elif os.path.isfile(path):
            return "file"

class BasicReducer:
    """Class of reducers (class methods) that make simple changes to state
    
    BasicReducer holds reducer functions, which make basic changes to the state dictionary.
    The reducers in this class are meant to be simple, changing only a few key values.
    The reducers assume the input state dictionary has all the necessary keys and does not sanitize the inputs.
    (The KeyBindReducer class will have the more complicated reducers)
    """

    @staticmethod
    def getInitState():
        """ Returns a state dictionary which is the initial state of application
        
        This is a special reducer called in the very beginning of runtime
            which sets the initial state of the application.
        Therefore it does not have any inputs, but it returns a state dictionary as output.

        Returns:
            dict: A state dictionary representing initial state of application  
        """
        newState = {}
        newState["directory"] = FileSystem.currentDir()
        newState["children"] = FileSystem.listDir(newState["directory"])
        newState["selected"] = newState["children"][0:1]
        newState["scroll_data"] = {
            "list_size": 40,
            "list_width": 100,
            "scroll_trigger": 3,
            "scroll_top": 0
        }
        newState["prompt_data"] = {
            "cmd_prompt": "(Command):",
            "brs_prompt": "(Browse) "
        }
        newState["mode"] = "browse"
        newState["text"] = newState["prompt_data"]["brs_prompt"] + "SP File Explorer"
        LOGGER.debug(f"Generated initial app state = {newState}")
        return newState
    
    @staticmethod
    def sameState(state):
        """ A reducer which returns a copy of the input state

        This reducer makes a deep copy of the input state dictionary
        and returns it, to indicate that the state has not changed.

        Args:
            state (dict): State dictionary of application at previous moment

        Returns:
            dict: State dictionary which represents nothing being changed
        """
        return copy.deepcopy(state) 

    @classmethod
    def setModeToBrowse(cls, state, text):
        """ A reducer which sets the application to browse mode, and displays text
        
        This reducer takes in an input state and a string.
        It first makes a deep copy of the input state.
        Then, it sets the state['mode'] to 'browse' and sets state['text'] 
            to the concatenation of state['prompt_data']['brs_prompt'] and the input text.

        Args:
            state (dict): State dictionary of application at previous moment
            text (str): Text to be displayed in text widget (after brs_prompt) 
 
        Returns:
            dict: State dictionary which represents browse mode to be activated and text message to be displayed
        """
        newState = cls.sameState(state)
        newState["mode"] = "browse"
        newState["text"] = newState["prompt_data"]["brs_prompt"] + text
        #LOGGER.info(f"Changed app state to browse mode")
        #LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def setModeToCommand(cls, state, text):
        """ A reducer which sets the application to command mode and displays text

        This reducer takes in an input state and a string.
        It first makes a deep copy of the input state.
        Then, it sets the state['mode'] to 'command' and sets state['text']
            to the concatenation of state['prompt_data']['cmd_prompt'] and the input text.

        Args:
            state (dict): State dictionary of application at previous moment
            text (str): Text to be displayed in text widget (after cmd_prompt) 
 
        Returns:
            dict: State dictionary which represents command mode to be activated and text message to be displayed
        """
        newState = cls.sameState(state)
        newState["mode"] = "command"
        newState["text"] = newState["prompt_data"]["cmd_prompt"] + text
        #LOGGER.info(f"Changed app state to command mode")
        #LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def deleteText(cls, state):
        """ A reducer which deletes a character from state["text"]

        The reducer takes in an input state.
        It first makes a deep copy of the input state,
            and then sets state["text"] to state["text"][0:len(state["text"])-1],
            i.e. it deletes the last character from state["text"].

        Args:
            state (dict): State dictionary of application at previous moment
            
        Returns:
            dict: State dictionary which represents a character being deleted from displayed text 
        
        Note:
            This reducer assumes state["text"] is not the empty string.
            This reducer will break if state["text"] is empty.
        """
        newState = cls.sameState(state)
        cmd_length = len(state["text"])
        newState["text"] = state["text"][0:cmd_length-1]
        return newState

    @classmethod
    def addText(cls, state, char):
        """ A reducer which adds a character to state["text"]

        This reducer takes in an input state and a string.
        It first makes a deep copy of the input state,
            and appends the input string to  state["text"].
        
        Args:
            state (dict): State dictionary of application at previous moment
            text (str): Character to be appended to the displayed text 

        Returns:
            dict: State dictionary which represents a character appended to displayed text

        Note:
            This reducer assumes char has length 1, 
                and that is how the reducer will be used generally,
                but it won't break if char has a different length.
        """
        newState = cls.sameState(state)
        newState["text"] += char
        return newState 
   
    @classmethod
    def moveDir(cls, state, dir):
        """ A reducer which changes the directory and children being viewed by application.

        This reducer takes in an input state and filepath to a directory.
        It first makes a deep copy of input state,
            and then sets the state["directory"] to dir.
        It calls on FileSystem.listDir to list the children of directory dir,
            and the list is set to state["children"]
        
        Args:
            state (dict): State dictionary of application at previous moment
            dir (str): Filepath of directory to be viewed by application

        Returns:
            dict: State dictionary which represents a directory and its children to be viewed by the application

        Note:
            This reducer assumes dir is a filepath to a directory. 
            This reducer will break if 
                (1) dir is not a string filepath
                or 
                (2) dir is a filepath to a file that is not a directory.
        """
        newState = cls.sameState(state)
        newState["directory"] = dir
        newState["children"] = FileSystem.listDir(dir)
        newState["selected"] = []
        return newState

    @classmethod
    def moveSelection(cls, state, indices):
        """ A reducer which changes the children files selected in application

        This reducer takes in an input state and a list of indices (integers).
        It first makes a deep copy of the input state,
            and then sets state["selected"] to include state["children"][i]
                for every i in the indices list.
        
        Args:
            state (dict): State dictionary of application at previous moment
            indices (str): List of indices (integers)

        Returns:
            dict: State dictionary which represents children files (indicated by indices list) which are selected in application.

        Note:
            This reducer assumes all the integers in indices
                are between 0 and len(state["children"]) - 1 inclusive.
            This reducer will break if that is not true.
        """
        newState = cls.sameState(state)
        newState["selected"] = [newState["children"][i] for i in indices]
        return newState

    @classmethod
    def moveScrollDown(cls, state):
        """ A reducer which moves scrolling down to match selection

        This reducer takes in an input state.
        It first makes a deep copy of the input state,
            and then sets the state["scroll_data"]["scroll_top"] to be such that
            the last selected child will be T-1 rows from the *bottom* of the list window.
        T is the state["scroll_data"]["scroll_trigger"].

        Args:
            state (dict): State dictionary of application at previous moment
            
        Returns:
            dict: State dictionary which represents the list window being scrolled down appropriately.

        Note:
            This reducer assumes that state["selected"] is not empty.
            This reducer will break if that is not true.
        """ 
        newState = cls.sameState(state)
        index = newState["children"].index(newState["selected"][-1]) 
        numc = len(newState["children"])
        size = newState["scroll_data"]["list_size"]
        trig = newState["scroll_data"]["scroll_trigger"]
        newState["scroll_data"]["scroll_top"] = min(max(0, index-size+trig), numc-size)
        return newState

    @classmethod
    def moveScrollUp(cls, state):
        """ A reducer which moves scrolling up to match selection

        This reducer takes in an input state.
        It first makes a deep copy of the input state,
            and then sets the state["scroll_data"]["scroll_top"] to be such that
            the last selected child will be T-1 rows from the *top* of the list window.
        T is the state["scroll_data"]["scroll_trigger"].

        Args:
            state (dict): State dictionary of application at previous moment
            
        Returns:
            dict: State dictionary which represents the list window being scrolled up appropriately.

        Note:
            This reducer assumes that state["selected"] is not empty.
            This reducer will break if that is not true.
        """
        newState = cls.sameState(state)
        index = newState["children"].index(newState["selected"][-1])
        numc = len(newState["children"])
        size = newState["scroll_data"]["list_size"]
        trig = newState["scroll_data"]["scroll_trigger"]
        newState["scroll_data"]["scroll_top"] = min(max(0, index-trig+1), numc-size)
        return newState
   
    @classmethod
    def setScrollDefault(cls, state):
        """ A reducer which moves scrolling to top

        This reducer takes in an input state.
        It first makes a deep copy of the input state,
            and then sets state["scroll_data"]["scroll_top"] to 0,
            which will make the first child in children list to be on the first row of the visible list window.
        This means the list scrollbar moves to the top.
        
        Args:
            state (dict): State dictionary of application at previous moment
            
        Returns:
            dict: State dictionary which represents the list window being scrolled to the top.
        """
        newState = cls.sameState(state)
        newState["scroll_data"]["scroll_top"] = 0
        return newState 
 
    @classmethod
    def quit(cls, state):
        """ A reducer which set application to quit mode.

        This reducer takes in an input state.
        It first makes a deep copy, and sets state["mode"] to "quit".
        When the output state is passed to Renderer, the Renderer will immediately destroy the application.
        
        Args:
            state (dict): State dictionary of application at previous moment
            
        Returns:
            dict: State dictionary which represents the application to be quit.
        """
        newState = cls.sameState(state)
        newState["mode"] = "quit"
        return newState

        
class KeyBindReducer:

    @staticmethod
    def deleteKey(state):
        if state["mode"] == "command" and state["text"] == state["prompt_data"]["cmd_prompt"]:
            return BasicReducer.setModeToBrowse(state, "SP File Explorer")
        elif state["mode"] == "command":
            return BasicReducer.deleteText(state)
        else: 
            return BasicReducer.sameState(state)

    @staticmethod
    def key(state, event):
        if state["mode"] == "command":
            return BasicReducer.addText(state, event.char)
        else:
            return BasicReducer.sameState(state) 

    @staticmethod
    def upKey(state):
        if state["mode"] == "browse" and len(state["selected"]) != 0:
            index = state["children"].index(state["selected"][-1])
            newState = BasicReducer.setModeToBrowse(state, "Moved Selection Up")
            if index != 0:
                newIndex = index - 1
                newState = BasicReducer.moveSelection(newState, [newIndex])
                wIndex = newIndex - newState["scroll_data"]["scroll_top"]
                trig = newState["scroll_data"]["scroll_trigger"]  
                if wIndex < trig - 1:
                    newState = BasicReducer.moveScrollUp(newState)
            return newState
        else:
            return BasicReducer.sameState(state) 
            
    @staticmethod
    def downKey(state):
        if state["mode"] == "browse" and len(state["selected"]) != 0:
            index = state["children"].index(state["selected"][-1]) 
            numc = len(state["children"])
            newState = BasicReducer.setModeToBrowse(state, "Moved Selection Down")
            if index != numc-1:
                newIndex = index + 1
                wIndex = newIndex - newState["scroll_data"]["scroll_top"]
                numw = state["scroll_data"]["list_size"]
                trig = state["scroll_data"]["scroll_trigger"]  
                newState = BasicReducer.moveSelection(newState, [newIndex])
                if wIndex > numw - trig:
                    newState = BasicReducer.moveScrollDown(newState)
            return newState
        else:
            return BasicReducer.sameState(state) 

    @staticmethod
    def shiftUpKey(state):
        parent = FileSystem.parent(state["directory"])
        LOGGER.debug(f"\t parent is {parent}")
        newState = BasicReducer.moveDir(state, parent)
        newState = BasicReducer.setModeToBrowse(newState, "Moved Up Directory")
        if len(newState["children"]) > 0:
            newState = BasicReducer.moveSelection(newState, [0])
            newState = BasicReducer.moveScrollUp(newState) 
        else:
            newState = BasicReducer.setScrollDefault(newState)
        return newState 
   
    @staticmethod
    def shiftDownKey(state):
        if len(state["selected"]) > 0:
            child_path = FileSystem.pathOfChild(state["directory"], state["selected"][-1])
            openable = FileSystem.isChildOpenable(child_path)
            if openable:
                newState = BasicReducer.moveDir(state, child_path)
                newState = BasicReducer.setModeToBrowse(newState, "Moved Down Directory")
                if len(newState["children"]) > 0:
                    newState = BasicReducer.moveSelection(newState, [0])
                    newState = BasicReducer.moveScrollUp(newState) 
                else:
                    newState = BasicReducer.setScrollDefault(newState)
                return newState
            else:
                return BasicReducer.sameState(state)          
        else:
            return BasicReducer.sameState(state) 
    
    @staticmethod
    def returnKey(state):
        length = len(state["prompt_data"]["cmd_prompt"])
        tokens = state["text"][length:].split()
        if len(tokens) >= 1 and tokens[0] == "mvdir":
            if len(tokens) >= 2 and tokens[1] == "up":
                return BasicReducer.moveUpDir(state)
            elif len(tokens) >= 2 and tokens[1] == "down":
                return BasicReducer.moveDownDir(state)
        elif len(tokens) >= 1 and tokens[0] == "mvsel":
            if len(tokens) >= 2 and tokens[1] == "up":
                return BasicReducer.moveUpSelection(state)
            elif len(tokens) >= 2 and tokens[1] == "down":
                return BasicReducer.moveDownSelection(state)
        return BasicReducer.changeModeToBrowse(state, "Error - Unrecognized Command")

    @staticmethod
    def colonKey(state):
        if state["mode"] == "browse":
            return BasicReducer.changeModeToCommand(state, "")

    @staticmethod
    def escapeSelectKeys(state):
        return BasicReducer.sameState(state)

class Renderer:
   
    @staticmethod
    def _render_label(app, state):
        dir = state["directory"]
        LOGGER.debug(f"Rendering application - Setting Label to current directory")
        app.label.configure(text=dir)
        LOGGER.debug(f"Rendering application - current directory is {dir}")
    
    @staticmethod
    def _render_listbox_items(app, state):
        dir = state["directory"]
        num_children = len(state["children"])
        LOGGER.debug(f"Rendering application - Setting Listbox to contain children")
        app.listbox.delete(0, END)
        LOGGER.debug(f"Rendering application - children list is {state['children']} of length {num_children}")
        for child in state["children"]:
            path = FileSystem.pathOfChild(dir, child)
            dirorfile = FileSystem.dirOrFile(path) 
            if dirorfile == "file":
                LOGGER.debug(f"{child} is a file")
                app.listbox.insert(END, child)
                app.listbox.itemconfig(END, background="yellow", selectbackground="orange")
            else:
                LOGGER.debug(f"{child}/ is a directory")
                app.listbox.insert(END, child + "/") 

    @staticmethod
    def _select_selected_children(app, state):
        LOGGER.debug(f"Rendering application - selecting children")
        LOGGER.debug(f"Rendering application - selected children list is {state['selected']}")
        for child in state["selected"]:
            index = state["children"].index(child)
            app.listbox.selection_set(index)
         
    @staticmethod
    def _set_scroll_position(app, state):
        num_children = len(state["children"])
        LOGGER.debug(f"Rendering application - setting scroll")
        fraction = state["scroll_data"]["scroll_top"] / (num_children + 1)
        app.listbox.yview_moveto(fraction)
        LOGGER.debug(f"Rendering application - scroll fraction is {fraction}")
            
    @staticmethod
    def _render_text(app, state):
        LOGGER.debug(f"Rendering application - Setting text")
        app.text.configure(state=NORMAL)
        app.text.delete("1.0", END)
        app.text.insert(END, state["text"])                 
        LOGGER.debug(f"Rendering application - Text is {state['text']}")
        LOGGER.debug(f"Rendering application - App is is {state['mode']} mode")
        if state["mode"] != "command":        
            app.text.configure(state=DISABLED)
            app.root.focus_set()
        else:
            app.text.focus_set()    

    @staticmethod
    def _save_state_in_app(app, state):
        LOGGER.debug(f"Rendering application - Saving state dictionary")
        app.state = state
        LOGGER.debug(f"Rendering application - State: {app.state}")

    @staticmethod
    def _set_sizes_of_listbox(app, state):
        LOGGER.debug(f"Rendering application - Sizing listbox widget")
        app.listbox.configure(width=state["scroll_data"]["list_width"], height=state["scroll_data"]["list_size"])
        LOGGER.debug(f"Rendering application - Listbox width is {state['scroll_data']['list_width']} characters") 
        LOGGER.debug(f"Rendering application - Listbox height is {state['scroll_data']['list_size']} lines")

    @staticmethod
    def _check_quit_mode(app, state):
        if state["mode"] == "quit":
            LOGGER.info(f"Quitting Application")
            app.root.destroy()
            sys.exit(0)

    @classmethod
    def render(cls, app, state):
        LOGGER.info(f"Rendering application")
        cls._check_quit_mode(app, state)
        cls._save_state_in_app(app, state)
        cls._set_sizes_of_listbox(app, state)
        cls._render_label(app, state)
        cls._render_listbox_items(app, state)
        cls._select_selected_children(app, state)
        cls._set_scroll_position(app, state)
        cls._render_text(app, state)
        
    
class Application:
    
    def initUI(app, root):
        LOGGER.info("Initializing User Interface")
        app.root = root 
        app.root.wm_title("Simple Python File Explorer")
        app.root.rowconfigure(1, weight=1)
        app.root.columnconfigure(0, weight=1)

        LOGGER.debug("Initializing User Interface - Creating scrollable listbox which expands horizontally and vertically with root window")
        app.listbox = Listbox(app.root, background="white", activestyle="dotbox", takefocus=0)
        app.listbox.grid(row=1, column=0, sticky=N+S+E+W) 
        
        app.scrollbar = Scrollbar(app.root, orient=VERTICAL, takefocus=0)
        app.scrollbar.grid(row=1, column=1, sticky=N+S) 
        
        app.listbox.configure(yscrollcommand=app.scrollbar.set)
        #app.scrollbar["command"] = app.listbox.yview
        
        LOGGER.debug("Initializing User Interface - Creating top label which expands horizontally with root window")
        app.label = Label(app.root, height=1, background="white", takefocus=0)
        app.label.grid(row=0, columnspan=2, sticky=W+E)
         
        LOGGER.debug("Initializing User Interface - Creating top text which expands horizontally with root window")
        app.text = Text(app.root, height=1, background="white", wrap=NONE, takefocus=0)
        app.text.grid(row=2, columnspan=2, sticky=W+E)


    def bindCallbacks(app):
        LOGGER.info(f"Binding Callbacks")
        #app.root.bind("-", lambda event: app.render(Reducers.moveUpDir(app.state)))
        #app.root.bind("<Return>", lambda event: app.render(Reducers.moveDownDir(app.state)))
        LOGGER.debug(f"Binding virtual event of listbox selection with mouse to changeModeToBrowse reducer - so the mouse does not affect selection")
        app.root.bind("<<ListboxSelect>>", lambda event: Renderer.render(app, KeyBindReducer.escapeSelectKeys(app.state)))
        app.root.bind("<Escape>", lambda event: Renderer.render(app, KeyBindReducer.escapeSelectKeys(app.state)))
        app.root.bind("<BackSpace>", lambda event: Renderer.render(app, KeyBindReducer.deleteKey(app.state)))
        app.root.bind("<Key>", lambda event: Renderer.render(app, KeyBindReducer.key(app.state, event)))
        app.root.bind("<Return>", lambda event: Renderer.render(app, KeyBindReducer.returnKey(app.state)))
         
        app.root.bind("<Up>", lambda event: Renderer.render(app, KeyBindReducer.upKey(app.state)))
        app.root.bind("<Down>", lambda event: Renderer.render(app, KeyBindReducer.downKey(app.state)))
        
        app.root.bind("<Shift-Up>", lambda event: Renderer.render(app, KeyBindReducer.shiftUpKey(app.state)))
        app.root.bind("<Shift-Down>", lambda event: Renderer.render(app, KeyBindReducer.shiftDownKey(app.state)))
        
        #LOGGER.debug(f"Binding ':' key to changeModeToCommand reducer")
        #app.root.bind(":", lambda event: Renderer.render(app, KeyBindReducer.colonKey(app.state)))
        
        #app.root.bind("<Down>", lambda event: app.render(Reducers.moveDownSelection(app.state)))
        #app.listbox.bind("<Up>", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Up>", lambda event: app.render(Reducers.moveUpSelection(app.state)))
        #app.root.bind("g", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Shift-KeyPress-G>", lambda event: app.render(Reducers.moveBottomSelection(app.state)))
        #app.root.bind("q", lambda event: app.render(Reducers.quit(app.state)))

    def __init__(app, root):
        app.state = BasicReducer.getInitState()
        app.initUI(root)
        Renderer.render(app, app.state)
        app.bindCallbacks()


if __name__ == "__main__":
    LOGGER.info("Starting Application")
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
