from os import listdir, sep, getcwd
from os.path import getmtime, getsize, isdir, isfile, islink, dirname, join
from time import localtime
from tkinter import Tk, Label, Listbox, Scrollbar, N, S, E, W, VERTICAL, END, DISABLED, NORMAL, Text, NONE, INSERT, DISABLED

"""
State represented as a python dictionary.

"""

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
        return newState
    
    """
    @staticmethod
    def moveUpDir(state):
        newState = {}
        newState["dir"] = dirname(state["dir"])
        newState["children"] = listdir(newState["dir"])
        newState["selected"] = newState["children"][0:1]
        newState["scroll_top"] = 0
        return newState

    @staticmethod
    def moveDownDir(state):
        if len(state["selected"]) != 0:
            newState = {}
            newState["dir"] = join(state["dir"],  state["selected"][0])
            newState["children"] = listdir(newState["dir"])
            newState["selected"] = newState["children"][0:1]
            newState["scroll_top"] = 0
            return newState
        else:
            return state

    @classmethod
    def moveDownSelection(cls, state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]

        selected = state["selected"][0]
        index = state["children"].index(selected)
        if index == len(state["children"]) - 1:
            new_index = index 
        else:
            new_index = index + 1            
        newState["selected"] = newState["children"][new_index:new_index+1]

        newState["scroll_top"] = state["scroll_top"]
        window_index = new_index - state["scroll_top"]
        num_children = len(newState["children"])
        if cls.list_size - window_index < cls.scroll_trigger and num_children - index >= cls.scroll_trigger:
            newState["scroll_top"] += 1
        return newState

    @classmethod
    def moveUpSelection(cls, state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]
        
        selected = state["selected"][0]
        index = state["children"].index(selected)
        if index == 0: 
            new_index = index
        else:
            new_index = index - 1
        newState["selected"] = newState["children"][new_index:new_index+1]
             
        newState["scroll_top"] = state["scroll_top"]
        window_index = new_index - state["scroll_top"]
        if window_index < cls.scroll_trigger and new_index >= cls.scroll_trigger:
            newState["scroll_top"] -= 1
        return newState

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
    def render(app, state):
        app.state = state
        
        if state["mode"] == "quit":
            app.root.destroy()
            return
        
        app.listbox.configure(width=state["scroll_data"]["list_width"], height=state["scroll_data"]["list_size"])

        dir = state["directory"]
        num_children = len(state["children"])
        app.label.configure(text=dir)
        app.listbox.delete(0, END)
        for child in state["children"]:
            path = join(dir, child)
            if isfile(path):
                app.listbox.insert(END, child)
                app.listbox.itemconfig(END, background="yellow", selectbackground="orange")
            elif isdir(path):
                app.listbox.insert(END, child + "/") 
        
        for child in state["selected"]:
            index = state["children"].index(child)
            app.listbox.selection_set(index)
            
        app.listbox.yview_moveto(state["scroll_data"]["scroll_top"] / (num_children + 1))
        
        app.text.delete(1.0, END)
        app.text.insert(INSERT, state["text"])                 
        app.text.config(state=DISABLED)

class Application:
    
    def initUI(self, root):
        self.root = root 
        self.root.wm_title("Simple Python File Explorer")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.listbox = Listbox(self.root, background="white", activestyle="dotbox", takefocus=0)
        self.listbox.grid(row=1, column=0, sticky=N+S+E+W) 
        
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, takefocus=0)
        self.scrollbar.grid(row=1, column=1, sticky=N+S) 
        
        self.label = Label(self.root, height=1, background="white", takefocus=0)
        self.label.grid(row=0, columnspan=2, sticky=W+E)
         
        self.text = Text(self.root, height=1, background="white", wrap=NONE, takefocus=0)
        self.text.grid(row=2, columnspan=2, sticky=W+E)

        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar["command"] = self.listbox.yview

    def bindCallbacks(self):
        #self.root.bind("-", lambda event: self.render(Reducers.moveUpDir(self.state)))
        #self.root.bind("<Return>", lambda event: self.render(Reducers.moveDownDir(self.state)))
        #self.root.bind("<<ListboxSelect>>", lambda event: Renderer.render(self, self.state))
        #self.root.bind("<Down>", lambda event: self.render(Reducers.moveDownSelection(self.state)))
        #self.listbox.bind("<Up>", lambda event: self.render(Reducers.moveTopSelection(self.state)))
        #self.root.bind("<Up>", lambda event: self.render(Reducers.moveUpSelection(self.state)))
        #self.root.bind("g", lambda event: self.render(Reducers.moveTopSelection(self.state)))
        #self.root.bind("<Shift-KeyPress-G>", lambda event: self.render(Reducers.moveBottomSelection(self.state)))
        #self.root.bind("q", lambda event: self.render(Reducers.quit(self.state)))

    def __init__(self, root):
        self.state = Reducers.getInitState()
        self.initUI(root)
        Renderer.render(self, self.state)
        self.bindCallbacks()


if __name__ == "__main__":
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
