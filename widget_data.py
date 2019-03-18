"""Module: widget_data

This module contains dictionaries of the visual information
    of every widget used in sp_file_explorer
"""
from tkinter import Button, Frame, Label, Listbox, Scrollbar,\
    TOP, BOTTOM, LEFT, RIGHT, X, BOTH, SINGLE, VERTICAL


MAIN_FRAME_DATA = {
    "widget_type": Frame,
    "attrs": {
        "background": "grey"
    },
    "pack_attrs": {
        "side": TOP,
        "fill": BOTH
    }
}

FILELIST_FRAME_DATA = {
    "widget_type": Frame,
    "attrs": {
        "background": "white",
        "borderwidth": 3,
        "relief": "ridge"
    },
    "pack_attrs": {
        "side": TOP,
        "fill": BOTH,
        #"padx": 5,
        #"pady": 5
    }

}

BUTTONS_FRAME_DATA = {
    "widget_type": Frame,
    "attrs": {
        "background": "grey"
    },
    "pack_attrs": {
        "side": TOP,
        "fill": BOTH,
        #"padx": 5,
        #"pady": 5
    }
}

SCROLL_LIST_FRAME_DATA = {
    "widget_type": Frame,
    "attrs": {
        "background": "grey"
    },
    "pack_attrs": {
        "side": BOTTOM,
        "fill": BOTH,
    }
}

UP_BUTTON_DATA = {
    "widget_type": Button,
    "attrs": {
        "text": "Move Up",
        "width": 9,
        "height": 1,
    },
    "pack_attrs": {
        "side": LEFT,
        "fill": X
    }
}

DOWN_BUTTON_DATA = {
    "widget_type": Button,
    "attrs": {
        "text": "Move Down",
        "width": 9,
        "height": 1,
    },
    "pack_attrs": {
        "side": LEFT,
        "fill": X
    }
}

CLOSE_BUTTON_DATA = {
    "widget_type": Button,
    "attrs": {
        "text": "Close",
        "width": 9,
        "height": 1,
    },
    "pack_attrs": {
        "side": RIGHT,
        "fill": X
    }
}

DIRECTORY_LABEL_DATA = {
    "widget_type": Label,
    "attrs": {
        "width": 90,
        "height": 1,
        "background": "white",
    },
    "pack_attrs": {
        "side": TOP,
        "fill": BOTH
    }
}

FILE_LISTBOX_DATA = {
    "widget_type": Listbox,
    "attrs": {
        "width": 96,
        "height": 33,
        "background": "white",
        "activestyle": "dotbox",
        "selectmode": SINGLE
    },
    "pack_attrs": {
        "side": LEFT,
        "fill": BOTH
    }
}

FILE_SCROLLBAR_DATA = {
    "widget_type": Scrollbar,
    "attrs": {
        "orient": VERTICAL
    },
    "pack_attrs": {
        "side": RIGHT,
        "fill": BOTH
    }
}
