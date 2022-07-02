from tkinter import *
import tkinter.ttk as ttk
import PandasMod
# from datetime import datetime, date


class DepositTreeview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # 1. 카운터 레이블
        self.lblDepositCount = Label(self)
        self.lblDepositCount.config(text=str(0))
        self.lblDepositCount.pack(side='top', anchor='e', padx=20)

        self.scrollbar_deposit = Scrollbar(self)
        self.scrollbar_deposit.pack(side="right", fill="y")

        self.treeviewDeposit = ttk.Treeview(self, selectmode="extended",
                                            yscrollcommand=self.scrollbar_deposit.set)

        self.treeviewDeposit.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar_deposit.config(command=self.treeviewDeposit.yview)
        # 입금내역 트리뷰 설정
        self.treeviewDeposit["columns"] = ("번호", "입금일", "보낸분", "입금액")

        self.treeviewDeposit.column('#0', width=0, stretch=NO)
        self.treeviewDeposit.column('번호', anchor=CENTER, width=50)
        self.treeviewDeposit.column('입금일', anchor=W, width=100)
        self.treeviewDeposit.column('보낸분', anchor=W, width=100)
        self.treeviewDeposit.column('입금액', anchor=E, width=100)

        self.treeviewDeposit.heading('#0')
        self.treeviewDeposit.heading('번호', text='번호', anchor=CENTER)
        self.treeviewDeposit.heading('입금일', text='입금일', anchor=CENTER)
        self.treeviewDeposit.heading('보낸분', text='보낸분', anchor=CENTER)
        self.treeviewDeposit.heading('입금액', text='입금액', anchor=CENTER)

        self.treeviewDeposit.tag_configure('oddrow', background='white')
        self.treeviewDeposit.tag_configure('evenrow', background='lightgray')

    def get_all(self):
        iids = self.treeviewDeposit.get_children()
        items = {}
        for iid in iids:
            items[iid] = self.treeviewDeposit.set(iid)
        return items

    def get_selected(self):
        items = {}
        iids = self.treeviewDeposit.selection()
        for iid in iids:
            items[int(iid)] = self.treeviewDeposit.set(iid)
        return items

    def get_focus(self):
        item = {}
        iid = self.treeviewDeposit.focus()
        item[iid] = self.treeviewDeposit.set(iid)
        return item

    def set(self, dp_dict):
        i = 0
        for idx in dp_dict:
            if i % 2 == 0:
                self.treeviewDeposit.insert(parent='', index='end', iid=idx, text='',
                                            values=(dp_dict[idx]['번호'], dp_dict[idx]['입금일'].date(),
                                                    dp_dict[idx]['보낸분'],
                                                    PandasMod.translate_currency(dp_dict[idx]['입금액'])),
                                            tags=('evenrow',))
            else:
                self.treeviewDeposit.insert(parent='', index='end', iid=idx, text='',
                                            values=(dp_dict[idx]['번호'], dp_dict[idx]['입금일'].date(),
                                                    dp_dict[idx]['보낸분'],
                                                    PandasMod.translate_currency(dp_dict[idx]['입금액'])),
                                            tags=('oddrow',))
            i += 1

        self.set_count()

    def set_count(self):
        count = len(self.treeviewDeposit.get_children())
        self.lblDepositCount.config(text=str(count))

    def reset(self):
        self.treeviewDeposit.delete(*self.treeviewDeposit.get_children())

    def update_treeview_deposit(self, dp_dict):
        self.reset()
        self.set(dp_dict)
        
        
if __name__ == '__main__':
    app = Tk()
    app_widget = DepositTreeview(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
