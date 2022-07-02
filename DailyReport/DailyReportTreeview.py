from tkinter import *
import tkinter.ttk as ttk
import PandasMod


class DailyReportTreeview(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.count = Frame(self)
        self.count.pack(side='top', fill='x')

        self.btn_set_dr_info_from_treeview = Button(self.count, text='운행일보 정보 로드',
                                                    command=self.set_dr_info_to_widget_by_treeview)
        self.btn_set_dr_info_from_treeview.pack(side='left', ipadx=5, ipady=5, padx=5, pady=5)

        self.lbl_treeview_daily_report_count = Label(self.count, width=4)
        self.lbl_treeview_daily_report_count.pack(side='right')
        self.lbl_treeview_daily_report_count.config(text=str(0))

        self.scrollbar_treeview_daily_report_list = Scrollbar(self)
        self.scrollbar_treeview_daily_report_list.pack(side="right", fill="y")

        self.treeview_daily_report = ttk.Treeview(self, height=10, selectmode="browse",
                                                  yscrollcommand=self.scrollbar_treeview_daily_report_list.set)
        self.treeview_daily_report.bind('<ButtonRelease-1>', self.set_daily_report_info_to_text_by_treeview)
        self.treeview_daily_report.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar_treeview_daily_report_list.config(command=self.treeview_daily_report.yview)
        # 트리뷰 설정
        self.treeview_daily_report["columns"] = ("일보ID", "배차시간", "상차지", "하차지", "화주명")
        # , "대표", "업태", "종목", "사업장주소", "전화번호", "우편번호", "우편주소", "이메일")

        self.treeview_daily_report.column('#0', width=0, stretch=NO)
        self.treeview_daily_report.column('일보ID', anchor=CENTER, width=30)
        self.treeview_daily_report.column('배차시간', anchor=W, width=100)
        self.treeview_daily_report.column('상차지', anchor=W, width=100)
        self.treeview_daily_report.column('하차지', anchor=W, width=100)
        self.treeview_daily_report.column('화주명', anchor=W, width=40)
        # self.treeview_daily_report.column('업태', anchor=W, width=40)
        # self.treeview_daily_report.column('종목', anchor=W, width=40)
        # self.treeview_daily_report.column('사업장주소', anchor=W, width=120)
        # self.treeview_daily_report.column('전화번호', anchor=W, width=50)
        # self.treeview_daily_report.column('우편번호', anchor=W, width=50)
        # self.treeview_daily_report.column('우편주소', anchor=W, width=120)
        # self.treeview_daily_report.column('이메일', anchor=W, width=50)

        self.treeview_daily_report.heading('#0')
        self.treeview_daily_report.heading('일보ID', text='ID', anchor=CENTER)
        self.treeview_daily_report.heading('배차시간', text='상차일', anchor=W)
        self.treeview_daily_report.heading('상차지', text='상차지', anchor=W)
        self.treeview_daily_report.heading('하차지', text='하차지', anchor=W)
        self.treeview_daily_report.heading('화주명', text='화주명', anchor=W)
        # self.treeview_daily_report.heading('대표', text='대표', anchor=W)
        # self.treeview_daily_report.heading('종목', text='종목', anchor=W)
        # self.treeview_daily_report.heading('사업장주소', text='사업장주소', anchor=W)
        # self.treeview_daily_report.heading('전화번호', text='전화번호', anchor=W)
        # self.treeview_daily_report.heading('우편번호', text='우편번호', anchor=W)
        # self.treeview_daily_report.heading('우편주소', text='우편주소', anchor=W)
        # self.treeview_daily_report.heading('이메일', text='이메일', anchor=W)

        self.treeview_daily_report.tag_configure('oddrow', background='white')
        self.treeview_daily_report.tag_configure('evenrow', background='lightgray')

    def get(self):
        pass

    def reset(self):
        self.treeview_daily_report.delete(*self.treeview_daily_report.get_children())

    def treeview_daily_report_selection_remove(self):
        iid = self.treeview_daily_report.focus()
        self.treeview_daily_report.selection_remove(iid)

    def set_dr_info_to_widget_by_treeview(self):
        if self.treeview_daily_report.focus():
            iid = self.treeview_daily_report.focus()
            str_idx = self.treeview_daily_report.set(iid)['일보ID']
            print(type(str_idx))
            idx = int(str_idx)

            dr_dicts = PandasMod.get_series_from_xl(idx, '운행일보', '일보ID', return_to_dict=True)
            dr_dict = dr_dicts[list(dr_dicts.keys())[0]]

            csn_idx = dr_dict['화주ID']

            csn_dicts = PandasMod.get_series_from_xl(csn_idx, '운송사목록', '화주ID', return_to_dict=True)
            pay_dicts = PandasMod.get_series_from_xl(idx, '세금계산서', '일보ID', return_to_dict=True)

            csn_dict = csn_dicts[list(csn_dicts.keys())[0]]
            pay_dict = pay_dicts[list(pay_dicts.keys())[0]]
            pay_dict.update({'전자세금계산서':''})

            print('\n\n========================')
            print('운행일보')
            for idx in dr_dict:
                print(f'{idx}: {dr_dict[idx]}')
            print('========================\n\n')
            print('운송사목록')
            for idx in csn_dict:
                print(f'{idx}: {csn_dict[idx]}')
            print('========================\n\n')
            print('세금계산서')
            for idx in pay_dict:
                print(f'{idx}: {pay_dict[idx]}')
            print('========================\n\n')

            self.master.master.freightInfo.set(dr_dict)
            self.master.master.consignorInfo.set(csn_dict)
            self.master.master.paymentInfo.set(pay_dict)

        else:
            print(False)

    def set_daily_report_info_to_text_by_treeview(self, event):
        if self.treeview_daily_report.focus():
            iid = self.treeview_daily_report.focus()
            str_idx = self.treeview_daily_report.set(iid)['일보ID']
            idx = int(str_idx)
            dr_dicts = PandasMod.get_series_from_xl(idx, '운행일보', '일보ID', return_to_dict=True)
            dr_dict = dr_dicts[list(dr_dicts.keys())[0]]
            pay_dicts = PandasMod.get_series_from_xl(idx, '세금계산서', '일보ID', return_to_dict=True)
            pay_dict = pay_dicts[list(pay_dicts.keys())[0]]
            dr_dict.update(pay_dict)
            self.master.master.drTreeviewInfo.set(dr_dict)

        else:
            print(False)

    def update_treeview_daily_report(self):
        dr_dict = PandasMod.get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '운행일보', return_by_dict=True)
        self.reset()
        self.set(dr_dict)

    def set(self, dr_dict):
        i = 1
        for idx in dr_dict:
            if i % 2 == 0:
                self.treeview_daily_report.insert(parent='', index='end', iid=idx, text='',
                                                  values=(dr_dict[idx]['일보ID'], dr_dict[idx]['배차시간'].date(),
                                                          dr_dict[idx]['상차지'], dr_dict[idx]['하차지'],
                                                          dr_dict[idx]['화주명']),
                                                  tags=('evenrow',))
                self.treeview_daily_report.see(idx)
            else:
                self.treeview_daily_report.insert(parent='', index='end', iid=idx, text='',
                                                  values=(dr_dict[idx]['일보ID'], dr_dict[idx]['배차시간'].date(),
                                                          dr_dict[idx]['상차지'], dr_dict[idx]['하차지'],
                                                          dr_dict[idx]['화주명']),
                                                  tags=('oddrow',))
                self.treeview_daily_report.see(idx)
            i += 1

        self.set_count()

    def set_count(self):
        count = len(self.treeview_daily_report.get_children())
        self.lbl_treeview_daily_report_count.config(text=str(count))


if __name__ == '__main__':
    app = Tk()
    freight_info = DailyReportTreeview(app)
    freight_info.config()
    freight_info.pack()

    app.mainloop()
