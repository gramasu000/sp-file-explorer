from sys import exit
import os
import copy
#from os import listdir, getcwd
#from os.path import getmtime, getsize, isdir, isfile, islink, dirname, join
#from copy import deepcopy
#from time import localtime
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

class FileSystem:

    @staticmethod
    def currentDir():
        return os.getcwd()

    @staticmethod
    def listDir(dir):
        return os.listdir(dir)

    @staticmethod
    def parent(path):
        return os.path.dirname(path)

    @staticmethod
    def pathOfChild(dir, child):
        return os.path.join(dir, child)

    @staticmethod
    def isChildOpenable(path):
        return os.path.isdir(path)        

    @staticmethod
    def dirOrFile(path):
        if os.path.isdir(path):
            return "dir"
        elif os.path.isfile(path):
            return "file"

class BasicReducers:

    @staticmethod
    def getInitState():
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
        return copy.deepcopy(state) 

    @classmethod
    def setModeToBrowse(cls, state, text):
        newState = cls.sameState(state)
        newState["mode"] = "browse"
        newState["text"] = newState["prompt_data"]["brs_prompt"] + text
        #LOGGER.info(f"Changed app state to browse mode")
        #LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def setModeToCommand(cls, state, text):
        newState = cls.sameState(state)
        newState["mode"] = "command"
        newState["text"] = newState["prompt_data"]["cmd_prompt"] + text
        #LOGGER.info(f"Changed app state to command mode")
        #LOGGER.debug(f"changed {state} to {newState}")
        return newState

    @classmethod
    def deleteText(cls, state):
        newState = cls.sameState(state)
        cmd_length = len(state["text"])
        newState["text"] = state["text"][0:cmd_length-1]
        return newState

    @classmethod
    def addText(cls, state, char):
        newState = cls.sameState(state)
        newState["text"] += char
        return newState 
   
    @classmethod
    def moveDir(cls, state, dir):
        newState = cls.sameState(state)
        newState["directory"] = dir
        newState["children"] = FileSystem.listDir(dir)
        newState["selected"] = []
        return newState

    @classmethod
    def moveSelection(cls, state, indices):
        newState = cls.sameState(state)
        newState["selected"] = [newState["children"][i] for i in indices]
        return newState

    @classmethod
    def moveScrollDown(cls, state):
        newState = cls.sameState(state)
        index = newState["children"].index(newState["selected"][-1]) 
        numc = len(newState["children"])
        size = newState["scroll_data"]["list_size"]
        trig = newState["scroll_data"]["scroll_trigger"]
        newState["scroll_data"]["scroll_top"] = min(max(0, index-size+trig), numc-size)
        return newState

    @classmethod
    def moveScrollUp(cls, state):
        newState = cls.sameState(state)
        index = newState["children"].index(newState["selected"][-1])
        numc = len(newState["children"])
        size = newState["scroll_data"]["list_size"]
        trig = newState["scroll_data"]["scroll_trigger"]
        newState["scroll_data"]["scroll_top"] = min(max(0, index-trig+1), numc-size)
        return newState
   
    @classmethod
    def setScrollDefault(cls, state):
        newState = cls.sameState(state)
        newState["scroll_data"]["scroll_top"] = 0
        return newState 
 
    @classmethod
    def quit(cls, state):
        newState = cls.sameState(state)
        newState["mode"] = "quit"
        return newState

        
class KeyBindReducers:

    @staticmethod
    def deleteKey(state):
        if state["mode"] == "command" and state["text"] == state["prompt_data"]["cmd_prompt"]:
            return BasicReducers.setModeToBrowse(state, "SP File Explorer")
        elif state["mode"] == "command":
            return BasicReducers.deleteText(state)
        else: 
            return BasicReducers.sameState(state)

    @staticmethod
    def key(state, event):
        if state["mode"] == "command":
            return BasicReducers.addText(state, event.char)
        else:
            return BasicReducers.sameState(state) 

    @staticmethod
    def upKey(state):
        if state["mode"] == "browse" and len(state["selected"]) != 0:
            index = state["children"].index(state["selected"][-1])
            newState = BasicReducers.setModeToBrowse(state, "Moved Selection Up")
            if index != 0:
                newIndex = index - 1
                newState = BasicReducers.moveSelection(newState, [newIndex])
                wIndex = newIndex - newState["scroll_data"]["scroll_top"]
                trig = newState["scroll_data"]["scroll_trigger"]  
                if wIndex < trig - 1:
                    newState = BasicReducers.moveScrollUp(newState)
            return newState
        else:
            return BasicReducers.sameState(state) 
            
    @staticmethod
    def downKey(state):
        if state["mode"] == "browse" and len(state["selected"]) != 0:
            index = state["children"].index(state["selected"][-1]) 
            numc = len(state["children"])
            newState = BasicReducers.setModeToBrowse(state, "Moved Selection Down")
            if index != numc-1:
                newIndex = index + 1
                wIndex = newIndex - newState["scroll_data"]["scroll_top"]
                numw = state["scroll_data"]["list_size"]
                trig = state["scroll_data"]["scroll_trigger"]  
                newState = BasicReducers.moveSelection(newState, [newIndex])
                if wIndex > numw - trig:
                    newState = BasicReducers.moveScrollDown(newState)
            return newState
        else:
            return BasicReducers.sameState(state) 

    @staticmethod
    def shiftUpKey(state):
        parent = FileSystem.parent(state["directory"])
        LOGGER.debug(f"\t parent is {parent}")
        newState = BasicReducers.moveDir(state, parent)
        newState = BasicReducers.setModeToBrowse(newState, "Moved Up Directory")
        if len(newState["children"]) > 0:
            newState = BasicReducers.moveSelection(newState, [0])
            newState = BasicReducers.moveScrollUp(newState) 
        else:
            newState = BasicReducers.setScrollDefault(newState)
        return newState 
   
    @staticmethod
    def shiftDownKey(state):
        if len(state["selected"]) > 0:
            child_path = FileSystem.pathOfChild(state["directory"], state["selected"][-1])
            openable = FileSystem.isChildOpenable(child_path)
            if openable:
                newState = BasicReducers.moveDir(state, child_path)
                newState = BasicReducers.setModeToBrowse(newState, "Moved Down Directory")
                if len(newState["children"]) > 0:
                    newState = BasicReducers.moveSelection(newState, [0])
                    newState = BasicReducers.moveScrollUp(newState) 
                else:
                    newState = BasicReducers.setScrollDefault(newState)
                return newState
            else:
                return BasicReducers.sameState(state)          
        else:
            return BasicReducers.sameState(state) 
    
    @staticmethod
    def returnKey(state):
        length = len(state["prompt_data"]["cmd_prompt"])
        tokens = state["text"][length:].split()
        if len(tokens) >= 1 and tokens[0] == "mvdir":
            if len(tokens) >= 2 and tokens[1] == "up":
                return BasicReducers.moveUpDir(state)
            elif len(tokens) >= 2 and tokens[1] == "down":
                return BasicReducers.moveDownDir(state)
        elif len(tokens) >= 1 and tokens[0] == "mvsel":
            if len(tokens) >= 2 and tokens[1] == "up":
                return BasicReducers.moveUpSelection(state)
            elif len(tokens) >= 2 and tokens[1] == "down":
                return BasicReducers.moveDownSelection(state)
        return BasicReducers.changeModeToBrowse(state, "Error - Unrecognized Command")

    @staticmethod
    def colonKey(state):
        if state["mode"] == "browse":
            return BasicReducers.changeModeToCommand(state, "")

    @staticmethod
    def escapeSelectKeys(state):
        return BasicReducers.sameState(state)

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
        app.root.bind("<<ListboxSelect>>", lambda event: Renderer.render(app, KeyBindReducers.escapeSelectKeys(app.state)))
        app.root.bind("<Escape>", lambda event: Renderer.render(app, KeyBindReducers.escapeSelectKeys(app.state)))
        app.root.bind("<BackSpace>", lambda event: Renderer.render(app, KeyBindReducers.deleteKey(app.state)))
        app.root.bind("<Key>", lambda event: Renderer.render(app, KeyBindReducers.key(app.state, event)))
        app.root.bind("<Return>", lambda event: Renderer.render(app, KeyBindReducers.returnKey(app.state)))
         
        app.root.bind("<Up>", lambda event: Renderer.render(app, KeyBindReducers.upKey(app.state)))
        app.root.bind("<Down>", lambda event: Renderer.render(app, KeyBindReducers.downKey(app.state)))
        
        app.root.bind("<Shift-Up>", lambda event: Renderer.render(app, KeyBindReducers.shiftUpKey(app.state)))
        app.root.bind("<Shift-Down>", lambda event: Renderer.render(app, KeyBindReducers.shiftDownKey(app.state)))
        
        #LOGGER.debug(f"Binding ':' key to changeModeToCommand reducer")
        #app.root.bind(":", lambda event: Renderer.render(app, KeyBindReducers.colonKey(app.state)))
        
        #app.root.bind("<Down>", lambda event: app.render(Reducers.moveDownSelection(app.state)))
        #app.listbox.bind("<Up>", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Up>", lambda event: app.render(Reducers.moveUpSelection(app.state)))
        #app.root.bind("g", lambda event: app.render(Reducers.moveTopSelection(app.state)))
        #app.root.bind("<Shift-KeyPress-G>", lambda event: app.render(Reducers.moveBottomSelection(app.state)))
        #app.root.bind("q", lambda event: app.render(Reducers.quit(app.state)))

    def __init__(app, root):
        app.state = BasicReducers.getInitState()
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
