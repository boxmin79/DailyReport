from tkinter import Menu
# import Tkinter as tk  # if using python 2


class MenuBar(Menu):
    def __init__(self, master):
        Menu.__init__(self, master)

        self.fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Exit", command=self.app_quit)

        self.editMenu = Menu(self, tearoff=False)
        self.add_cascade(label='Edit', menu=self.editMenu)
        self.editMenu.add_command(label='underEdit1')
        self.editMenu.add_separator()
        self.editMenu.add_command(label='underEdit2')

        self.functionMenu = Menu(self, tearoff=False)
        self.add_cascade(label='Function', menu=self.functionMenu)
        self.functionMenu.add_command(label='운행일보', command=self.call_daily_report)
        self.functionMenu.add_command(label='세금계산서 관리', command=self.call_tax_invoice_manager)
        self.functionMenu.add_command(label='입금 관리', command=self.call_deposit_manager)
        self.functionMenu.add_command(label='비용 관리', command=self.call_cost_manager)

    def app_quit(self):
        self.master.app_quit()

    def call_daily_report(self):
        self.master.call_daily_report()

    def call_tax_invoice_manager(self):
        self.master.call_tax_invoice_manager()

    def call_deposit_manager(self):
        self.master.call_deposit_manager()

    def call_cost_manager(self):
        self.master.call_cost_manager()


if __name__ == '__main__':
    from tkinter import Tk

    root = Tk()
    root.title("OCR_GUI")
    # root.geometry('1900x1040')
    root.resizable(True, True)

    menubar = MenuBar(root)
    root.config(menu=menubar)

    root.mainloop()