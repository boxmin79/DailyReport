from tkinter import *
import PandasMod
import ExcelMod


class TaxInvoiceButton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.btn_to_iti_get_list = Button(self, text='목록가져오기', width=15, command=self.load_before_issue_dict)
        self.btn_to_iti_print = Button(self, text='세금계산서 인쇄', width=15, command=self.print_iti)
        self.btn_to_iti_preview = Button(self, text='세금계산서 미리보기', width=15)
        self.btn_to_envelop_print = Button(self, text='우편봉투 인쇄', width=15, command=self.print_envelop)
        self.btn_not_deposit_list = Button(self, text='미입금 리스트', width=15, command=self.not_deposit_list)
        self.btn_close = Button(self, text='종료', width=15, command=self.quit)

        self.btn_to_iti_get_list.pack(side='left', anchor='w', padx=5, pady=5, ipadx=3, ipady=3)
        self.btn_to_iti_print.pack(side='left', padx=3, pady=5, ipadx=3, ipady=3)
        self.btn_to_iti_preview.pack(side='left', padx=3, pady=5, ipadx=3, ipady=3)
        self.btn_to_envelop_print.pack(side='left', padx=3, pady=5, ipadx=3, ipady=3)
        self.btn_not_deposit_list.pack(side='left', padx=5, pady=5, ipadx=3, ipady=3)
        self.btn_close.pack(side='right', anchor='e', expand=True, padx=15, pady=5, ipadx=3, ipady=3)

    def load_before_issue_dict(self):
        self.master.before_issue_dict = PandasMod.get_before_issue_dict()
        self.master.timTreeview.set(self.master.before_issue_dict)
        self.master.print_dict = PandasMod.get_print_dict(self.master.before_issue_dict)

    def print_iti(self):
        ExcelMod.print_iti(self.master.print_dict)

    def print_envelop(self):
        ExcelMod.print_envelop(self.master.print_dict)
        ExcelMod.record_iti_date(self.master.print_dict)

    def not_deposit_list(self):
        ExcelMod.not_deposit_list()

    def app_quit(self):
        self.master.app_quit()


if __name__ == '__main__':
    app = Tk()
    app_widget = TaxInvoiceButton(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
