from tkinter import Tk, Frame
import StatusBar
import TaxInvoiceTreeview
import TaxInvoiceButton


class TaxInvoiceManager(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.before_issue_dict = {}
        self.print_dict = {}

        # 1. bottom(상태바) 프레임
        self.stausBar = StatusBar.StatusBar(self)
        self.stausBar.config(bg='gray')
        self.stausBar.pack(side='bottom', fill='x')

        # 2. 세금계산서 리스트박스 프레임
        self.timTreeview = TaxInvoiceTreeview.TaxInvoiceTreeview(self)
        self.timTreeview.config()
        self.timTreeview.pack(side='top', fill='both')

        # 3. 하단 버튼들
        self.timButton = TaxInvoiceButton.TaxInvoiceButton(self)
        self.timButton.config()
        self.timButton.pack(side='top', fill='x')

    def quit(self):
        self.master.quit()


if __name__ == '__main__':
    app = Tk()
    app_widget = TaxInvoiceManager(app)
    app_widget.config()
    app_widget.pack(expand=True, fill='both')

    app.mainloop()
