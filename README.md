# sp-file-explorer (Simple Python File Explorer)

sp-file-explorer is a file explorer app with keybindings (no mouse clicks) written in Python.

The application does make use of the following libraries 
   
 - tkinter
 - os
 - logging
 - unittest
 - copy

all of which are available from a standard python installation.
It does not make use of libraries outside what is available in Python's Standard Library,
so it should work on any machine which runs python.

## To Use

Run the python script file 
```
$ python sp_file_explorer.py
```

## Pictures

Here is how the application looks in a Windows 10 machine.

![windows-picture](notes/pic1.jpg)

Here is how the application looks in an Arch Linux machine running Awesome WM.

![arch-picture](notes/pic2.jpg)

## Keybindings

### Browse Mode

The following four basic keybindings are supported when application is in browse mode.

 - Up Arrow Key: Move selection up
 - Down Arrow Key: Move selection down
 - Shift-Up: Ascend to parent directory
 - Shift-Down: Descend to child directory

### Command Mode

Furthermore, the colon key can be used to go into command mode, 
in which the user will type a command which will open a file.

#### General

In general, if the app selection is on a file `somefile` and if the user types 

```
:some shell command
```

and presses Enter, this is equivalent to running the following command

```
$ some shell command somefile & 
``` 
#### Examples

If the app selection is on a file named `example.pdf`, the user can type the following

```
:mupdf
```

and press Enter to have the `mupdf` program open `example.pdf` independently from the app.

If the app selection is on `main.cpp`, the user can type the following

```
:xterm -e vim
```

and press Enter to launch an independent xterm terminal opening `main.cpp` using vim text editor. 

