from tkinter import *
import tkinter.ttk as ttk
import PandasMod


class CostManagerTreeview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # 1. 카운터 레이블
        self.lblCostTreeviewCount = Label(self)
        self.lblCostTreeviewCount.config(text=str(0))
        self.lblCostTreeviewCount.pack(side='top', anchor='e', padx=20)

        self.scrollbar_cost = Scrollbar(self)
        self.scrollbar_cost.pack(side="right", fill="y")

        self.treeviewCost = ttk.Treeview(self, selectmode="extended",
                                         yscrollcommand=self.scrollbar_cost.set)

        self.treeviewCost.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar_cost.config(command=self.treeviewCost.yview)
        # 미입금 리스트 트리뷰 설정
        self.treeviewCost["columns"] = ("날짜", "분류", "항목", "금액", "단가", "수량", "운행거리")

        self.treeviewCost.column('#0', width=0, stretch=NO)
        self.treeviewCost.column('날짜', anchor=CENTER, width=100)
        self.treeviewCost.column('분류', anchor=W, width=120)
        self.treeviewCost.column('항목', anchor=W, width=120)
        self.treeviewCost.column('금액', anchor=E, width=100)
        self.treeviewCost.column('단가', anchor=E, width=100)
        self.treeviewCost.column('수량', anchor=E, width=100)
        self.treeviewCost.column('운행거리', anchor=E, width=100)

        self.treeviewCost.heading('#0')
        self.treeviewCost.heading('날짜', text='날짜', anchor=CENTER)
        self.treeviewCost.heading('분류', text='분류', anchor=W)
        self.treeviewCost.heading('항목', text='항목', anchor=W)
        self.treeviewCost.heading('금액', text='금액', anchor=CENTER)
        self.treeviewCost.heading('단가', text='단가', anchor=CENTER)
        self.treeviewCost.heading('수량', text='수량', anchor=CENTER)
        self.treeviewCost.heading('운행거리', text='운행거리', anchor=CENTER)

        self.treeviewCost.tag_configure('oddrow', background='white')
        self.treeviewCost.tag_configure('evenrow', background='lightgray')

    def get_all(self):
        iids = self.treeviewCost.get_children()
        items = {}
        for iid in iids:
            items[iid] = self.treeviewCost.set(iid)
        return items
    
    def get_selected(self):
        iids = self.treeviewCost.selection()
        items = {}
        for iid in iids:
            items[iid] = self.treeviewCost.set(iid)
        return items
    
    def get_focus(self):
        return self.treeviewCost.set(self.treeviewCost.focus())

    def reset(self):
        self.treeviewCost.delete(*self.treeviewCost.get_children())
    
    def add(self, cost_dict):
        self.get_count()
        self.set(cost_dict, self.get_count() + 1)

    def set(self, cost_dict, i=0):
        for idx in cost_dict:
            if i % 2 == 0:
                self.treeviewCost.insert(parent='', index='end', iid=idx, text='',
                                         values=(cost_dict[idx]['날짜'].date(), cost_dict[idx]['분류'],
                                                 cost_dict[idx]['항목'],
                                                 PandasMod.translate_currency(cost_dict[idx]['금액']),
                                                 PandasMod.translate_currency(cost_dict[idx]['단가']),
                                                 cost_dict[idx]['수량'], cost_dict[idx]['운행거리']),
                                         tags=('evenrow',))
                self.treeviewCost.see(idx)
            else:
                self.treeviewCost.insert(parent='', index='end', iid=idx, text='',
                                         values=(cost_dict[idx]['날짜'].date(), cost_dict[idx]['분류'],
                                                 cost_dict[idx]['항목'],
                                                 PandasMod.translate_currency(cost_dict[idx]['금액']),
                                                 PandasMod.translate_currency(cost_dict[idx]['단가']),
                                                 cost_dict[idx]['수량'], cost_dict[idx]['운행거리']),
                                         tags=('oddrow',))
                self.treeviewCost.see(idx)
            i += 1

        self.set_count()
    
    def get_count(self):
        return len(self.treeviewCost.get_children())

    def set_count(self):
        self.lblCostTreeviewCount.config(text=str(self.get_count()))
    
    def update_treeview_cost(self, cost_dict):
        self.reset()
        self.set(cost_dict)


if __name__ == '__main__':
    app = Tk()
    app_widget = CostManagerTreeview(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
