from os import listdir, sep, getcwd
from os.path import getmtime, getsize, isdir, isfile, islink, dirname, join
from time import localtime
from tkinter import Tk, Label, Listbox, Scrollbar, N, S, E, W, VERTICAL, END, DISABLED, NORMAL

class Reducers:

    list_size = 40
    list_width = 100    
    scroll_trigger = 3

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
        

class Application:
    
    def initUI(self, root):
        self.root = root 
        self.root.wm_title("Simple Python File Explorer")
        self.root.configure(takefocus=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.listbox = Listbox(self.root, background="white", activestyle="dotbox", width=100, height=40)
        self.listbox.grid(row=1, column=0, sticky=N+S+E+W) 
        
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, takefocus=0)
        self.scrollbar.grid(row=1, column=1, sticky=N+S) 
        
        self.label = Label(self.root, height=1, background="white", takefocus=0)
        self.label.grid(row=0, columnspan=2, sticky=W+E)
         
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar["command"] = self.listbox.yview

    def render(self, state):
        # Save State
        self.state = state

        # Reset Directory Label
        dir = self.state["dir"]
        self.label.configure(text=dir)

        # Reset Listbox of children files
        self.listbox.delete(0, END)        
        
        for child in self.state["children"]:
            path = join(dir, child)
            if isfile(path):
                self.listbox.insert(END, child)
                self.listbox.itemconfig(END, background="yellow", selectbackground="orange")
            elif isdir(path):
                self.listbox.insert(END, child + "/") 
            elif islink(path):
                self.listbox.insert(END, child + "/ (L)")
                self.listbox.itemconfig(END, background="green", selectbackground="purple")
        
        # Select specified children
        for child in self.state["selected"]:
            index = self.state["children"].index(child)
            self.listbox.selection_set(index)
        
        # Set scroll
        fraction = self.state["scroll_top"] / (len(self.state["children"]) + 1)
        self.listbox.yview_moveto(fraction) 

    def bindCallbacks(self):
        self.root.bind("a", lambda event: self.render(Reducers.moveUpDir(self.state)))
        self.root.bind("z", lambda event: self.render(Reducers.moveDownDir(self.state)))
        self.root.bind("<<ListboxSelect>>", lambda event: self.render(self.state))
        self.root.bind("<Down>", lambda event: self.render(Reducers.moveDownSelection(self.state)))
        self.root.bind("<Up>", lambda event: self.render(Reducers.moveUpSelection(self.state)))

    def __init__(self, root):
        state = {
            "dir": getcwd(),
            "children": listdir(getcwd()),
            "selected": listdir(getcwd())[0:1],
            "scroll_top": 0  
        }
        self.initUI(root)
        self.render(state)
        self.bindCallbacks()


if __name__ == "__main__":
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
