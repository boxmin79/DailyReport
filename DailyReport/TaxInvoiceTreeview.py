from tkinter import *
import tkinter.font
import tkinter.ttk as ttk
import PandasMod


class TaxInvoiceTreeview(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.items = {}

        self.tiManager_columns = ('일보ID', '배차시간', '화주ID', '화주명', '운송료', '수수료',
                                  '결제방법', '합계금액', '계산서', '발행방법', '수금상태', '보낸분')

        # 1 타이틀프레임
        self.frm_tim_title = Frame(self)
        self.frm_tim_title.pack(side='top', anchor='n', fill='x')

        # 3-2타이틀 레이블
        self.font_title = tkinter.font.Font(family='맑은 고딕', size=20)
        self.lbl_tim_title = Label(self.frm_tim_title, text='세금계산서 발행할 목록', font=self.font_title)
        self.lbl_tim_title.pack(side='left')

        # 2 트리뷰
        # 2-1 프레임
        self.frm_tim_treeview = Frame(self)  # , relief='solid', bd=1)
        self.frm_tim_treeview.pack(side='top', anchor='n', fill='both')

        # 2-2 카운터 레이블
        self.frm_tim_count = Frame(self.frm_tim_treeview)  # , relief='solid', bd=1)
        self.frm_tim_count.pack(expand=True, fill='x', padx=5)

        self.lbl_tim_count_title = Label(self.frm_tim_count, text='count :')
        self.lbl_tim_count_title.pack(side='left', anchor='e', expand=True)

        self.lbl_tim_count = Label(self.frm_tim_count)
        self.lbl_tim_count.config(text=str(0))
        self.lbl_tim_count.pack(side='left', anchor='e')

        # 2-4 미발행 세금계산서 트리뷰
        self.scrbar_tim = Scrollbar(self.frm_tim_treeview)
        self.scrbar_tim.pack(side="right", fill="y")

        self.treeview_tim = ttk.Treeview(self.frm_tim_treeview, selectmode="extended",
                                         yscrollcommand=self.scrbar_tim.set)
        self.treeview_tim["columns"] = self.tiManager_columns
        # '일보ID', '배차시간', '화주ID', '화주명', '운송료', '수수료', '결제방법', '합계금액', '계산서', '발행방법', '수금상태', '보낸분'
        self.treeview_tim.pack(expand=True, fill="both", padx=5)

        self.treeview_tim.column('#0', width=0, stretch=NO)
        # self.treeview_tim.column('번호', anchor=CENTER, width=30)
        self.treeview_tim.column('일보ID', anchor=CENTER, width=100)
        self.treeview_tim.column('배차시간', anchor=CENTER, width=100)
        self.treeview_tim.column('화주ID', anchor=E, width=100)
        self.treeview_tim.column('화주명', anchor=W, width=120)
        self.treeview_tim.column('운송료', anchor=E, width=120)
        self.treeview_tim.column('수수료', anchor=E, width=120)
        self.treeview_tim.column('결제방법', anchor=CENTER, width=100)
        self.treeview_tim.column('합계금액', anchor=E, width=100)
        self.treeview_tim.column('계산서', anchor=CENTER, width=100)
        self.treeview_tim.column('발행방법', anchor=CENTER, width=100)
        self.treeview_tim.column('수금상태', anchor=CENTER, width=100)
        self.treeview_tim.column('보낸분', anchor=CENTER, width=100)

        self.treeview_tim.heading('#0')
        # self.treeview_tim.heading('번호', text='번호', anchor=CENTER)
        self.treeview_tim.heading('일보ID', text='일보ID', anchor=CENTER)
        self.treeview_tim.heading('배차시간', text='배차시간', anchor=CENTER)
        self.treeview_tim.heading('화주ID', text='화주ID', anchor=CENTER)
        self.treeview_tim.heading('화주명', text='화주명', anchor=CENTER)
        self.treeview_tim.heading('운송료', text='운송료', anchor=CENTER)
        self.treeview_tim.heading('수수료', text='수수료', anchor=CENTER)
        self.treeview_tim.heading('결제방법', text='결제방법', anchor=CENTER)
        self.treeview_tim.heading('합계금액', text='합계금액', anchor=CENTER)
        self.treeview_tim.heading('계산서', text='계산서', anchor=CENTER)
        self.treeview_tim.heading('발행방법', text='발행방법', anchor=CENTER)
        self.treeview_tim.heading('수금상태', text='수금상태', anchor=CENTER)
        self.treeview_tim.heading('보낸분', text='보낸분', anchor=CENTER)

        # 5. 리스트박스 config모음
        self.treeview_tim.tag_configure('oddrow', background='white')
        self.treeview_tim.tag_configure('evenrow', background='lightgray')

        self.scrbar_tim.config(command=self.treeview_tim.yview)

    def get(self):
        items = []
        iids = self.treeview_tim.get_children()
        for iid in iids:
            item = self.treeview_tim.set(iid)
            # print(record['운송료'])
            # print(record['수수료'])
            # print(record['합계금액'])
            item['일보ID'] = int(item['일보ID'])
            item['화주ID'] = int(item['화주ID'])
            item['운송료'] = PandasMod.currency_to_int(item['운송료'])
            item['수수료'] = PandasMod.currency_to_int(item['수수료'])
            item['합계금액'] = PandasMod.currency_to_int(item['합계금액'])
            items.append(item)

        return items

    def set_count(self):
        count = len(self.treeview_tim.get_children())
        self.lbl_tim_count.config(text=str(count))

    def update_treeview_tim(self, df):
        self.reset()
        self.set(df)

    def reset(self):
        self.treeview_tim.delete(*self.treeview_tim.get_children())

    def set(self, items):
        i = 0
        for idx in items:
            # print(record)
            # fare = PandasMod.translate_currency(df[idx]['운송료'])

            if i % 2 == 0:
                self.treeview_tim.insert(parent='', index='end', iid=idx, text='',
                                         values=(idx, items[idx]['배차시간'], items[idx]['화주ID'],
                                                 items[idx]['화주명'],
                                                 PandasMod.translate_currency(items[idx]['운송료']),
                                                 PandasMod.translate_currency(items[idx]['수수료']),
                                                 items[idx]['결제방법'],
                                                 PandasMod.translate_currency(items[idx]['합계금액']),
                                                 items[idx]['계산서'], items[idx]['발행방법'], items[idx]['수금상태'],
                                                 items[idx]['보낸분']),
                                         tags=('evenrow',))
            else:
                self.treeview_tim.insert(parent='', index='end', iid=idx, text='',
                                         values=(idx, items[idx]['배차시간'], items[idx]['화주ID'],
                                                 items[idx]['화주명'],
                                                 PandasMod.translate_currency(items[idx]['운송료']),
                                                 PandasMod.translate_currency(items[idx]['수수료']),
                                                 items[idx]['결제방법'],
                                                 PandasMod.translate_currency(items[idx]['합계금액']),
                                                 items[idx]['계산서'], items[idx]['발행방법'], items[idx]['수금상태'],
                                                 items[idx]['보낸분']),
                                         tags=('oddrow',))
            i += 1

        self.set_count()


if __name__ == '__main__':
    app = Tk()
    app_widget = TaxInvoiceTreeview(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
