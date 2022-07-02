from tkinter import *
import tkinter.ttk as ttk
import PandasMod


class ConsignorTreeview(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)
                
        self.count = Frame(self)
        self.count.pack(side='top', fill='x')

        self.btn_set_consignor_info_from_treeview = Button(self.count, text='운송사 정보 로드',
                                                           command=self.set_consignor_info_to_widget_by_treeview)
        self.btn_set_consignor_info_from_treeview.pack(side='left', ipadx=5, ipady=5, padx=5, pady=5)

        self.lbl_treeview_consignor_list_count = Label(self.count, width=4)
        self.lbl_treeview_consignor_list_count.pack(side='right')
        self.lbl_treeview_consignor_list_count.config(text=str(0))

        self.scrollbar_treeview_consignor_list = Scrollbar(self)
        self.scrollbar_treeview_consignor_list.pack(side="right", fill="y")

        self.treeview_consignor_list = ttk.Treeview(self, height=4, selectmode="browse",
                                                    yscrollcommand=self.scrollbar_treeview_consignor_list.set)
        self.treeview_consignor_list.bind('<ButtonRelease-1>', self.set_consignor_info_to_text_by_treeview)
        self.treeview_consignor_list.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar_treeview_consignor_list.config(command=self.treeview_consignor_list.yview)
        # 트리뷰 설정
        self.treeview_consignor_list["columns"] = ("화주ID", "화주명", "사업자번호", "상호명")
        # , "대표", "업태", "종목", "사업장주소", "전화번호", "우편번호", "우편주소", "이메일")

        self.treeview_consignor_list.column('#0', width=0, stretch=NO)
        self.treeview_consignor_list.column('화주ID', anchor=CENTER, width=30)
        self.treeview_consignor_list.column('화주명', anchor=W, width=100)
        self.treeview_consignor_list.column('사업자번호', anchor=W, width=100)
        self.treeview_consignor_list.column('상호명', anchor=W, width=100)
        # self.treeview_consignor_list.column('대표', anchor=W, width=40)
        # self.treeview_consignor_list.column('업태', anchor=W, width=40)
        # self.treeview_consignor_list.column('종목', anchor=W, width=40)
        # self.treeview_consignor_list.column('사업장주소', anchor=W, width=120)
        # self.treeview_consignor_list.column('전화번호', anchor=W, width=50)
        # self.treeview_consignor_list.column('우편번호', anchor=W, width=50)
        # self.treeview_consignor_list.column('우편주소', anchor=W, width=120)
        # self.treeview_consignor_list.column('이메일', anchor=W, width=50)

        self.treeview_consignor_list.heading('#0')
        self.treeview_consignor_list.heading('화주ID', text='ID', anchor=CENTER)
        self.treeview_consignor_list.heading('화주명', text='화주명', anchor=W)
        self.treeview_consignor_list.heading('사업자번호', text='사업자번호', anchor=W)
        self.treeview_consignor_list.heading('상호명', text='상호명', anchor=W)
        # self.treeview_consignor_list.heading('업태', text='업태', anchor=W)
        # self.treeview_consignor_list.heading('대표', text='대표', anchor=W)
        # self.treeview_consignor_list.heading('종목', text='종목', anchor=W)
        # self.treeview_consignor_list.heading('사업장주소', text='사업장주소', anchor=W)
        # self.treeview_consignor_list.heading('전화번호', text='전화번호', anchor=W)
        # self.treeview_consignor_list.heading('우편번호', text='우편번호', anchor=W)
        # self.treeview_consignor_list.heading('우편주소', text='우편주소', anchor=W)
        # self.treeview_consignor_list.heading('이메일', text='이메일', anchor=W)

        self.treeview_consignor_list.tag_configure('oddrow', background='white')
        self.treeview_consignor_list.tag_configure('evenrow', background='lightgray')

    def update_csn_same_list(self, csn_name):
        same_csn_dict = PandasMod.get_same_csn(csn_name)
        self.update_csn_treeview(same_csn_dict)

        if len(same_csn_dict) == 1:
            self.master.master.csnTreeviewInfo.reset()
            self.master.master.csnTreeviewInfo.set(same_csn_dict[list(same_csn_dict.keys())[0]])
        elif len(same_csn_dict) > 1 or len(same_csn_dict) == 0:
            self.master.master.csnTreeviewInfo.reset()

    def set_consignor_info_to_widget_by_treeview(self):
        print('Run <ConsignorTreeview.set_consignor_info_to_widget_by_treeview()')
        if self.treeview_consignor_list.focus():
            iid = self.treeview_consignor_list.focus()
            idx = int(self.treeview_consignor_list.set(iid)['화주ID'])
            csn_dict = PandasMod.get_series_from_xl(idx, '운송사목록', '화주ID', return_to_dict=True)
            print(csn_dict[list(csn_dict.keys())[0]])
            self.master.master.consignorInfo.set(csn_dict[list(csn_dict.keys())[0]])

        else:
            print(False)
        print('Done <ConsignorTreeview.set_consignor_info_to_widget_by_treeview()')

    def set_consignor_info_to_text_by_treeview(self, event):
        print('Run <ConsignorTreeview.set_consignor_info_to_text_by_treeview>')
        iid = self.treeview_consignor_list.focus()
        idx = int(self.treeview_consignor_list.set(iid)['화주ID'])
        # PandasMod.get_series_from_xl(idx, '운송사목록')
        self.master.master.csnTreeviewInfo.clear()
        get_csn_dict = PandasMod.get_series_from_xl(idx, '운송사목록', '화주ID', return_to_dict=True)
        print(f' get_csn_dict[list(get_csn_dict.keys())[0]] \n'
              f'{get_csn_dict[list(get_csn_dict.keys())[0]]}')
        self.master.master.csnTreeviewInfo.set(get_csn_dict[list(get_csn_dict.keys())[0]])
        print('Done <ConsignorTreeview.set_consignor_info_to_text_by_treeview>')

    def reset(self):
        self.treeview_consignor_list.delete(*self.treeview_consignor_list.get_children())
        # print('운송사 트리뷰가 reset 되었습니다.')

    def update_csn_treeview(self, csn_dict):
        self.reset()
        self.set(csn_dict)

    def set(self, csn_dict):
        # print(csn_dict)
        i = 0
        for idx in csn_dict:
            if i % 2 == 0:
                self.treeview_consignor_list.insert(parent='', index='end', iid=idx, text='',
                                                    values=(csn_dict[idx]['화주ID'], csn_dict[idx]['화주명'],
                                                            csn_dict[idx]['사업자번호'], csn_dict[idx]['상호']),
                                                    tags=('evenrow',))
            else:
                self.treeview_consignor_list.insert(parent='', index='end', iid=idx, text='',
                                                    values=(csn_dict[idx]['화주ID'], csn_dict[idx]['화주명'],
                                                            csn_dict[idx]['사업자번호'], csn_dict[idx]['상호']),
                                                    tags=('oddrow',))
            i += 1

        self.set_count()

    def set_count(self):
        count = len(self.treeview_consignor_list.get_children())
        self.lbl_treeview_consignor_list_count.config(text=str(count))


if __name__ == '__main__':
    app = Tk()
    freight_info = ConsignorTreeview(app)
    freight_info.config()
    freight_info.pack()

    app.mainloop()
