import tkinter
from tkinter import ttk

import sv_ttk

root = tkinter.Tk()


entry = tkinter.Entry(root, width=30)

button = ttk.Button(root, text="Click me!")
button.pack()

# This is where the magic happens
sv_ttk.set_theme("dark")


def get_data():
    return entry.get()


root.mainloop()