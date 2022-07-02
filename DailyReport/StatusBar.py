from tkinter import Frame
from tkinter import Label
from tkinter import StringVar


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.text_lbl_status = StringVar()
        self.lbl_status = Label(self, textvariable=self.text_lbl_status, bg='gray')
        self.lbl_status.pack(side='left')
        self.text_lbl_status.set('상태바')
