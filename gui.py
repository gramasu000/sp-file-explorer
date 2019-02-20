from tkinter import Tk, Frame, TOP, BOTH

gui_settings = {
    "r_mf_w": 800,
    "r_mf_h": 600,
    "mf_bg": "green",
    "ff_w": 790,
    "ff_h": 550,
    "ff_p": 5,
    "ff_bg": "white",
    "ff_bw": 3,
    "ff_r": "ridge",
    "bf_w": 790,
    "bf_h": 30,
    "bf_p": 5,
    "bf_bg": "orange"
}

class FileExplorerGUI:

    def __init__(self, parent, settings):
        self.root = parent
        self.main_frame = Frame(self.root)
        self.main_frame.configure(
            background=settings["mf_bg"], 
            width=settings["r_mf_w"], 
            height=settings["r_mf_h"]
        )
        self.main_frame.pack(side=TOP, fill=BOTH)
        
        self.flist_frame = Frame(self.main_frame)
        self.flist_frame.configure(
            background=settings["ff_bg"],
            width=settings["ff_w"],
            height=settings["ff_h"],
            borderwidth=settings["ff_bw"],
            relief=settings["ff_r"]
        )
        self.flist_frame.pack(
            side=TOP, 
            fill=BOTH, 
            padx=settings["ff_p"],
            pady=settings["ff_p"]
        )
        
        self.buttons_frame = Frame(self.main_frame)
        self.buttons_frame.configure(
            background=settings["bf_bg"],
            width=settings["bf_w"],
            height=settings["bf_h"],
        )
        self.buttons_frame.pack(
            side=TOP,
            fill=BOTH,
            padx=settings["bf_p"],
            pady=settings["bf_p"]
        )

root = Tk()
root.geometry(
    "{}x{}".format(gui_settings["r_mf_w"], gui_settings["r_mf_h"])
)

gui = FileExplorerGUI(root, gui_settings)
root.mainloop()
