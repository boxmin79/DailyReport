from tkinter import *
import tkinter.ttk as ttk
import PandasMod


class ReceivableTreeview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # 1. 카운터 레이블
        self.lblReceivableCount = Label(self)
        self.lblReceivableCount.config(text=str(0))
        self.lblReceivableCount.pack(side='top', anchor='e', padx=20)

        # 2. 트리뷰
        self.scrbar_receivable = Scrollbar(self)
        self.scrbar_receivable.pack(side="right", fill="y")

        self.treeviewReceivable = ttk.Treeview(self, selectmode="extended",
                                               yscrollcommand=self.scrbar_receivable.set)

        self.treeviewReceivable.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrbar_receivable.config(command=self.treeviewReceivable.yview)

        # 3. 미입금 리스트 트리뷰 설정
        self.treeviewReceivable["columns"] = ("일보ID", "배차시간", "화주명", "합계금액")

        self.treeviewReceivable.column('#0', width=0, stretch=NO)
        # self.treeviewReceivable.column('행번호', anchor=CENTER, width=50)
        self.treeviewReceivable.column('일보ID', anchor=CENTER, width=50)
        self.treeviewReceivable.column('배차시간', anchor=W, width=100)
        self.treeviewReceivable.column('화주명', anchor=W, width=100)
        self.treeviewReceivable.column('합계금액', anchor=E, width=100)

        self.treeviewReceivable.heading('#0')
        # self.treeviewReceivable.heading('행번호', text='행번호', anchor=CENTER)
        self.treeviewReceivable.heading('일보ID', text='일보ID', anchor=CENTER)
        self.treeviewReceivable.heading('배차시간', text='날짜', anchor=W)
        self.treeviewReceivable.heading('화주명', text='운송사', anchor=W)
        self.treeviewReceivable.heading('합계금액', text='운임', anchor=W)

        self.treeviewReceivable.tag_configure('oddrow', background='white')
        self.treeviewReceivable.tag_configure('evenrow', background='lightgray')

    def get_all(self):
        iids = self.treeviewReceivable.get_children()
        items = []
        for iid in iids:
            items.append(self.treeviewReceivable.set(iid))
        return items

    def get_selected(self):
        iids = self.treeviewReceivable.selection()
        items = {}
        for iid in iids:
            items[int(iid)] = self.treeviewReceivable.set(iid)
        return items

    def get_focus(self):
        iid = self.treeviewReceivable.focus()
        item = self.treeviewReceivable.set(iid)
        return item

    def set(self, re_dict):
        i = 0
        for idx in re_dict:
            if i % 2 == 0:
                self.treeviewReceivable.insert(parent='', index='end', iid=idx, text='',
                                               values=(re_dict[idx]['일보ID'], re_dict[idx]['배차시간'].date(),
                                                       re_dict[idx]['화주명'],
                                                       PandasMod.translate_currency(re_dict[idx]['합계금액'])),
                                               tags=('evenrow',))
            else:
                self.treeviewReceivable.insert(parent='', index='end', iid=idx, text='',
                                               values=(re_dict[idx]['일보ID'], re_dict[idx]['배차시간'].date(),
                                                       re_dict[idx]['화주명'],
                                                       PandasMod.translate_currency(re_dict[idx]['합계금액'])),
                                               tags=('oddrow',))
            i += 1

        self.set_count()

    def set_count(self):
        count = len(self.treeviewReceivable.get_children())
        self.lblReceivableCount.config(text=str(count))

    def reset(self):
        self.treeviewReceivable.delete(*self.treeviewReceivable.get_children())

    def update_receivable_treeview(self, re_dict):
        self.reset()
        self.set(re_dict)


if __name__ == '__main__':
    app = Tk()
    app_widget = ReceivableTreeview(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
