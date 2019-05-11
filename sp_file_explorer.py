from sys import exit
from os import listdir, sep, getcwd
from os.path import getmtime, getsize, isdir, isfile, islink, dirname, join
from time import localtime
from tkinter import Tk, Label, Listbox, Scrollbar, Text, N, S, E, W, VERTICAL, END, DISABLED, NORMAL, NONE, INSERT, DISABLED, StringVar
import logging

"""
State represented as a python dictionary.

"""
def initLogging(logger_name, logfile_name):
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


class Reducers:

    @staticmethod
    def getInitState():
        newState = {}
        newState["directory"] = getcwd()
        newState["children"] = listdir(newState["directory"])
        newState["selected"] = newState["children"][0:1]
        newState["scroll_data"] = {
            "list_size": 40,
            "list_width": 100,
            "scroll_trigger": 3,
            "scroll_top": 0
        }
        newState["mode"] = "browse"
        newState["text"] = "SP File Explorer"
        LOGGER.info(f"Generated initial app state")
        LOGGER.debug(f"Generated app state dictionary is {newState}")
        return newState
    
    @staticmethod
    def _deepCopy(state):
        newState = {}
        for key in state:
            newState[key] = state[key]
        return newState

    @classmethod
    def changeModeToBrowse(cls, state):
        newState = cls._deepCopy(state)
        newState["mode"] = "browse"
        newState["text"] = "SP File Explorer"
        LOGGER.info(f"Changed app state to browse mode")
        LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def changeModeToCommand(cls, state):
        newState = cls._deepCopy(state)
        newState["mode"] = "command"
        newState["text"] = ":"
        LOGGER.info(f"Changed app state to command mode")
        LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def _deleteText(cls, state):
        newState = cls._deepCopy(state)
        cmd_length = len(state["text"])
        newState["text"] = state["text"][0:cmd_length-1]
        return newState

    @classmethod
    def _addText(cls, state, char):
        newState = cls._deepCopy(state)
        newState["text"] += char
        return newState 

    @classmethod
    def deleteKey(cls, state):
        if state["mode"] == "command" and len(state["text"]) <= 1:
            return cls.changeModeToBrowse(state)
        elif state["mode"] == "command" and len(state["text"]) > 1:
            return cls._deleteText(state)
        else: 
            return cls._deepCopy(state)

    @classmethod
    def key(cls, state, event):
        if state["mode"] == "command":
            return cls._addText(state, event.char)
        else:
            return cls._deepCopy(state) 

    @classmethod
    def _moveUpDir(cls, state):
        newState = cls._deepCopy(state)
        newState["directory"] = dirname(state["directory"])
        newState["children"] = listdir(newState["directory"])
        newState["selected"] = newState["children"][0:1]
        newState["scroll_data"]["scroll_top"] = 0
        newState["mode"] = "browse"
        newState["text"] = "Moved up directory"
        return newState

    @classmethod
    def _moveDownDir(cls, state):
        newState = cls._deepCopy(state)
        if len(state["selected"]) != 0:
            newState["directory"] = join(state["directory"],  state["selected"][0])
            newState["children"] = listdir(newState["directory"])
            newState["selected"] = newState["children"][0:1]
            newState["scroll_data"]["scroll_top"] = 0
        newState["mode"] = "browse"
        newState["text"] = "Moved down directory"
        return newState
    
    @classmethod
    def _moveDownSelection(cls, state):
        newState = cls._deepCopy(state)
        if len(state["selected"]) != 0:
            selected = state["selected"][0]
            index = state["children"].index(selected)
            if index == len(state["children"]) - 1:
                new_index = index 
            else:
                new_index = index + 1            
            newState["selected"] = newState["children"][new_index:new_index+1]

            window_index = new_index - state["scroll_data"]["scroll_top"]
            num_children = len(newState["children"])
            if state["scroll_data"]["list_size"] - window_index < state["scroll_data"]["scroll_trigger"] and num_children - index >= state["scroll_data"]["scroll_trigger"]:
                newState["scroll_data"]["scroll_top"] += 1
        newState["mode"] = "browse"
        newState["text"] = "Moved selection down"
        return newState

    @classmethod
    def _moveUpSelection(cls, state):
        newState = cls._deepCopy(state)
       
        if len(state["selected"]) != 0: 
            selected = state["selected"][0]
            index = state["children"].index(selected)
            if index == 0: 
                new_index = index
            else:
                new_index = index - 1
            newState["selected"] = newState["children"][new_index:new_index+1]
        
            window_index = new_index - state["scroll_data"]["scroll_top"]
            if window_index < state["scroll_data"]["scroll_trigger"] and new_index >= state["scroll_data"]["scroll_trigger"]:
                newState["scroll_data"]["scroll_top"] -= 1
        newState["mode"] = "browse"
        newState["text"] = "Moved selection up"
        return newState

    @classmethod
    def returnKey(cls, state):
        if state["mode"] == "command":
            if state["text"] == ":mvdir up":
                return cls._moveUpDir(state)
            elif state["text"] == ":mvdir down":
                return cls._moveDownDir(state)
            elif state["text"] == ":mvsel up":
                return cls._moveUpSelection(state)
            elif state["text"] == ":mvsel down":
                return cls._moveDownSelection(state)
            else:    
                return cls.changeModeToBrowse(state)


    """
    @staticmethod
    def moveTopSelection(state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]
        newState["selected"] = state["children"][0:1]
        newState["scroll_top"] = 0
        return newState

    @classmethod
    def moveBottomSelection(cls, state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]
        num_children = len(newState["children"])
        newState["selected"] = state["children"][num_children-1:num_children]
        newState["scroll_top"] = num_children - cls.list_size
        return newState

    @staticmethod
    def quit(state):
        return {}  
    """

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
            path = join(dir, child)
            if isfile(path):
                LOGGER.debug(f"{child} is a file")
                app.listbox.insert(END, child)
                app.listbox.itemconfig(END, background="yellow", selectbackground="orange")
            elif isdir(path):
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
            exit(0)

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
        app.root.bind("<<ListboxSelect>>", lambda event: Renderer.render(app, Reducers.changeModeToBrowse(app.state)))
        app.root.bind("<Escape>", lambda event: Renderer.render(app, Reducers.changeModeToBrowse(app.state)))
        app.root.bind("<BackSpace>", lambda event: Renderer.render(app, Reducers.deleteKey(app.state)))
        app.root.bind("<Key>", lambda event: Renderer.render(app, Reducers.key(app.state, event)))
        app.root.bind("<Return>", lambda event: Renderer.render(app, Reducers.returnKey(app.state)))
         
        LOGGER.debug(f"Binding ':' key to changeModeToCommand reducer")
        app.root.bind(":", lambda event: Renderer.render(app, Reducers.changeModeToCommand(app.state)))
        
        #app.root.bind("<Down>", lambda event: app.render(Reducers.moveDownSelection(app.state)))
        #app.listbox.bind("<Up>", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Up>", lambda event: app.render(Reducers.moveUpSelection(app.state)))
        #app.root.bind("g", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Shift-KeyPress-G>", lambda event: app.render(Reducers.moveBottomSelection(app.state)))
        #app.root.bind("q", lambda event: app.render(Reducers.quit(app.state)))

    def __init__(app, root):
        app.state = Reducers.getInitState()
        app.initUI(root)
        Renderer.render(app, app.state)
        app.bindCallbacks()


if __name__ == "__main__":
    global LOGGER
    LOGGER = initLogging(__name__, "sp_file_explorer.log")
    print(LOGGER)
    LOGGER.info("Starting Application")
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
