from os import listdir, sep, getcwd
from os.path import getmtime, getsize, isdir, isfile, islink
from time import localtime
from tkinter import Tk, Label, Listbox, Scrollbar, N, S, E, W, VERTICAL, END

class Application:
    
    def initUI(self, root):
        self.root = root 
        self.root.wm_title("Simple Python File Explorer")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.label = Label(self.root, height=1, background="white")
        self.label.grid(row=0, columnspan=2, sticky=W+E)
        
        self.listbox = Listbox(self.root, background="white", activestyle="dotbox")
        self.listbox.grid(row=1, column=0, sticky=N+S+E+W) 
         
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.scrollbar.grid(row=1, column=1, sticky=N+S) 
        
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
        children = self.state["children"]
        for child in children:
            path = dir + sep + child
            self.listbox.insert(END, child)
            if isdir(path):
                self.listbox.itemconfig(END, background="yellow", selectbackground="orange")
            elif islink(path):
                self.listbox.itemconfig(END, background="green", selectbackground="purple")

    def bindCallbacks(self):
        # TODO
        pass


    def __init__(self, root):
        self.state = {
            "dir": getcwd(),
            "children": listdir(getcwd()) 
        }
        self.initUI(root)
        self.render(self.state)


if __name__ == "__main__":
    ROOT = Tk()
    APP = Application(ROOT)
    APP.root.mainloop()
