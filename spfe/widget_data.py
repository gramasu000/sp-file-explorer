"""Module containing visual information of widgets

This module contains python dictionaries containing
the visual and packing information for each widget in the app.
These dictionaries will be passed as argument
to the make_tk_widget function in the sp_file_explorer module 
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