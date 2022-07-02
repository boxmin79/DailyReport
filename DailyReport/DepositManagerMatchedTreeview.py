from tkinter import *
import tkinter.ttk as ttk
import PandasMod
# from datetime import datetime, date


class MatchedTreeview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # 1. 카운터 레이블
        self.lblMatchedCount = Label(self)
        self.lblMatchedCount.config(text=str(0))
        self.lblMatchedCount.pack(side='top', anchor='e', padx=20)

        # 2. 트리뷰
        self.scrollbar_match = Scrollbar(self)
        self.scrollbar_match.pack(side="right", fill="y")

        self.treeviewMatch = ttk.Treeview(self, selectmode="extended",
                                          yscrollcommand=self.scrollbar_match.set)

        self.treeviewMatch.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar_match.config(command=self.treeviewMatch.yview)
        # 매칭 트리뷰 설정
        self.treeviewMatch["columns"] = ("일보ID", "배차시간", "화주명", "합계금액", "빈칸", "입금일", "보낸분", "입금액",)

        self.treeviewMatch.column('#0', width=0, stretch=NO)
        self.treeviewMatch.column('일보ID', anchor=W, width=50)
        self.treeviewMatch.column('배차시간', anchor=W, width=100)
        self.treeviewMatch.column('화주명', anchor=W, width=100)
        self.treeviewMatch.column('합계금액', anchor=E, width=100)
        self.treeviewMatch.column('빈칸', anchor=CENTER, width=30)
        self.treeviewMatch.column('입금일', anchor=W, width=100)
        self.treeviewMatch.column('보낸분', anchor=W, width=100)
        self.treeviewMatch.column('입금액', anchor=E, width=100)

        self.treeviewMatch.heading('#0')
        self.treeviewMatch.heading('일보ID', text='일보ID', anchor=CENTER)
        self.treeviewMatch.heading('화주명', text='화주명', anchor=CENTER)
        self.treeviewMatch.heading('배차시간', text='배차시간', anchor=CENTER)
        self.treeviewMatch.heading('합계금액', text='합계금액', anchor=CENTER)
        self.treeviewMatch.heading('빈칸', text='==', anchor=CENTER)
        self.treeviewMatch.heading('입금일', text='입금일', anchor=CENTER)
        self.treeviewMatch.heading('보낸분', text='보낸분', anchor=CENTER)
        self.treeviewMatch.heading('입금액', text='입금액', anchor=CENTER)

        self.treeviewMatch.tag_configure('oddrow', background='white')
        self.treeviewMatch.tag_configure('evenrow', background='lightgray')

    def get_all(self):
        iids = self.treeviewMatch.get_children()
        items = {}
        for iid in iids:
            items[iid] = self.treeviewMatch.set(iid)
        return items

    def get_selected(self):
        iids = self.treeviewMatch.selection()
        items = {}
        for iid in iids:
            items[iid] = self.treeviewMatch.set(iid)
        return items

    def get_focus(self):
        iid = self.treeviewMatch.focus()
        item = self.treeviewMatch.set(iid)
        return item

    def add(self, mat_dict):
        count = len(self.treeviewMatch.get_children())
        self.set(mat_dict, count + 1)

    def set(self, mat_dict, i=0):
        for idx in mat_dict:
            if i % 2 == 0:
                self.treeviewMatch.insert(parent='', index='end', iid=idx, text='',
                                          values=(mat_dict[idx]['일보ID'], mat_dict[idx]['배차시간'].date(),
                                                  mat_dict[idx]['화주명'],
                                                  PandasMod.translate_currency(mat_dict[idx]['합계금액']),
                                                  mat_dict[idx]['빈칸'],
                                                  mat_dict[idx]['입금일'].date(), mat_dict[idx]['보낸분'],
                                                  PandasMod.translate_currency(mat_dict[idx]['입금액'])),
                                          tags=('evenrow',))
                self.treeviewMatch.see(idx)
            else:
                self.treeviewMatch.insert(parent='', index='end', iid=idx, text='',
                                          values=(mat_dict[idx]['일보ID'], mat_dict[idx]['배차시간'].date(),
                                                  mat_dict[idx]['화주명'],
                                                  PandasMod.translate_currency(mat_dict[idx]['합계금액']),
                                                  mat_dict[idx]['빈칸'],
                                                  mat_dict[idx]['입금일'].date(), mat_dict[idx]['보낸분'],
                                                  PandasMod.translate_currency(mat_dict[idx]['입금액'])),
                                          tags=('oddrow',))
                self.treeviewMatch.see(idx)
            i += 1

        self.set_count()

    def set_count(self):
        count = len(self.treeviewMatch.get_children())
        self.lblMatchedCount.config(text=str(count))

    def reset(self):
        self.treeviewMatch.delete(*self.treeviewMatch.get_children())

    def update_treeview_match(self, mat_dict):
        self.reset()
        self.set(mat_dict)


if __name__ == '__main__':
    app = Tk()
    app_widget = MatchedTreeview(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
