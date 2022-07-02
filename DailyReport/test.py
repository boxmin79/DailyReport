from tkinter import *
import DailyReportFilter


class Test(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.date_filter = DailyReportFilter.DailyReportFilter(self)
        self.date_filter.pack()

        # toplevel = Toplevel(self)
        # toplevel.geometry("320x200+820+100")


if __name__ == '__main__':
    app = Tk()
    app_widget = Test(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
