# -*- coding: utf-8 -*-
# File: hello1.py
# http://www.pythonware.com/library/tkinter/introduction/hello-tkinter.htm
import Tkinter
import tkFont


root = Tkinter.Tk()
font = tkFont.Font(size=100)
message="再见"
w = Tkinter.Label(root, text=message,font=font)
w.pack()

root.mainloop()
