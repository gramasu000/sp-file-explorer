from os import listdir, sep, getcwd
from os.path import getmtime, getsize, isdir, isfile, islink, dirname
from time import localtime
from tkinter import Tk, Label, Listbox, Scrollbar, N, S, E, W, VERTICAL, END, DISABLED, NORMAL

class Reducers:
    
    @staticmethod
    def moveUpDir(state):
        newState = {}
        newState["dir"] = dirname(state["dir"])
        newState["children"] = listdir(newState["dir"])
        newState["selected"] = newState["children"][0:1]
        return newState

    @staticmethod
    def moveDownDir(state):
        if len(state["selected"]) != 0:
            newState = {}
            newState["dir"] = state["dir"] + sep + state["selected"][0]
            newState["children"] = listdir(newState["dir"])
            newState["selected"] = newState["children"][0:1]
            return newState
        else:
            return state

    @staticmethod
    def moveDownSelection(state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]
        selected = state["selected"][0]
        index = state["children"].index(selected)
        if index == len(state["children"]) - 1: 
            newState["selected"] = newState["children"][index:index+1]
        else:
            newState["selected"] = newState["children"][index+1:index+2]
        return newState

    @staticmethod
    def moveUpSelection(state):
        newState = {}
        newState["dir"] = state["dir"]
        newState["children"] = state["children"]
        selected = state["selected"][0]
        index = state["children"].index(selected)
        if index == 0: 
            newState["selected"] = newState["children"][0:1]
        else:
            newState["selected"] = newState["children"][index-1:index]
        return newState
        

class Application:
    
    def initUI(self, root):
        self.root = root 
        self.root.wm_title("Simple Python File Explorer")
        self.root.geometry("800x600")
        self.root.configure(takefocus=0)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.listbox = Listbox(self.root, background="white", activestyle="dotbox")
        self.listbox.grid(row=1, column=0, sticky=N+S+E+W) 
        
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, takefocus=0)
        self.scrollbar.grid(row=1, column=1, sticky=N+S) 
        
        self.label = Label(self.root, height=1, background="white", takefocus=0)
        self.label.grid(row=0, columnspan=2, sticky=W+E)
         
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.listbox.yview

    def render(self, state):
        # Save State
        self.state = state

        # Reset Directory Label
        dir = self.state["dir"]
        self.label.configure(text=dir)

        # Reset Listbox of children files
        self.listbox.delete(0, END)        
        
        for child in self.state["children"]:
            path = dir + sep + child
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
            "selected": listdir(getcwd())[0:1]  
        }
        self.initUI(root)
        self.render(state)
        self.bindCallbacks()


if __name__ == "__main__":
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
