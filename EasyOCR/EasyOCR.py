from tkinter import *


class ClassName(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)


if __name__ == '__main__':
    app = Tk()
    app_widget = ClassName(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
