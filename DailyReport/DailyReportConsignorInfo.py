from tkinter import *
import PandasMod
import ExcelMod


class ConsignorInfo(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)
        self.csnColumns = ('화주ID', '화주명', '사업자번호', '상호', '대표자명', '업태', '업종', '사업장주소', '연락처',
                           '우편번호', '우편물주소', '전자우편', '전화번호2', '비고')  # 14

        self.out_frm = Frame(self, bg='#AAAAAA')
        self.out_frm.pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # 화주번호 ID
        self.frm_consignorID = Frame(self.out_frm)
        self.frm_consignorID.pack(fill='x')

        self.text_consignorID = StringVar()
        self.text_consignorID.set('')

        self.lbl_consignor_title = Label(self.frm_consignorID, text='번호 :', font=12)
        self.lbl_consignor_title.pack(side='left', expand=True, anchor='e')

        self.etr_consignorID = Entry(self.frm_consignorID, relief='flat', bg='#EEEEEE',
                                     textvariable=self.text_consignorID, width=0, justify='right', font=12)
        self.etr_consignorID.pack(side='left', anchor='e')

        self.innerFrame = Frame(self.out_frm, bg='#AAAAAA')
        self.innerFrame.pack(side='top', expand=True, fill='both', padx=1, pady=1)

        # 화주명
        self.innerFrame01 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame01.pack(side='top', fill='x')

        self.lbl_consignor = Label(self.innerFrame01, text='화주명', width=10, font=12)
        self.lbl_consignor.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_consignor = StringVar()
        self.etr_consignor = Entry(self.innerFrame01, textvariable=self.text_consignor, relief='flat', font=12)
        self.etr_consignor.bind('<FocusOut>', self.set_consignor_id_by_event)
        self.etr_consignor.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)
        # self.etr_consignor.bind('<Any-KeyRelease>', self.find_csn)

        # 사업자번호
        self.innerFrame02 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame02.pack(side='top', fill='x')

        self.lbl_business_number = Label(self.innerFrame02, text='사업자번호', width=10, font=12)
        self.lbl_business_number.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_business_number = StringVar()
        self.etr_business_number = Entry(self.innerFrame02, textvariable=self.text_business_number,
                                         relief='flat', font=12)
        self.etr_business_number.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)
        self.etr_business_number.bind('<Any-KeyRelease>', self.set_etr_business_number)

        # 상호
        self.innerFrame03 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame03.pack(side='top', fill='x')

        self.lbl_business_name = Label(self.innerFrame03, text='상호', width=10, font=12)
        self.lbl_business_name.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_business_name = StringVar()
        self.etr_business_name = Entry(self.innerFrame03, textvariable=self.text_business_name, relief='flat', font=12)
        self.etr_business_name.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 대표자명
        self.innerFrame04 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame04.pack(side='top', fill='x')

        self.lbl_owner_name = Label(self.innerFrame04, text='대표자명', width=10, font=12)
        self.lbl_owner_name.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_owner_name = StringVar()
        self.etr_owner_name = Entry(self.innerFrame04, textvariable=self.text_owner_name, relief='flat', font=12)
        self.etr_owner_name.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 업태, 업종
        self.innerFrame05 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame05.pack(side='top', fill='x')

        self.lbl_business_state = Label(self.innerFrame05, text='업태', width=10, font=12)
        self.lbl_business_state.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_business_state = StringVar()
        self.etr_business_state = Entry(self.innerFrame05, textvariable=self.text_business_state, relief='flat',
                                        width=14, font=12)
        self.etr_business_state.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        self.lbl_business_sector = Label(self.innerFrame05, text='업종', width=10, font=12)
        self.lbl_business_sector.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_business_sector = StringVar()
        self.etr_business_sector = Entry(self.innerFrame05, textvariable=self.text_business_sector, relief='flat',
                                         width=14, font=12)
        self.etr_business_sector.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 사업장주소
        self.innerFrame06 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame06.pack(side='top', fill='x')

        self.lbl_business_address = Label(self.innerFrame06, text='사업장주소', width=10, font=12)
        self.lbl_business_address.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_business_address = StringVar()
        self.etr_business_address = Entry(self.innerFrame06, textvariable=self.text_business_address,
                                          relief='flat', font=12)
        self.etr_business_address.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 전화번호
        self.innerFrame07 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame07.pack(side='top', fill='x')

        self.lbl_phone_number = Label(self.innerFrame07, text='연락처', width=10, font=12)
        self.lbl_phone_number.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_phone_number = StringVar()
        self.etr_phone_number = Entry(self.innerFrame07, validate="key", justify=RIGHT,
                                      textvariable=self.text_phone_number, relief='flat', font=12)
        # self.etr_phone_number['validatecommand'] = (self.etr_phone_number.register(testval), '%P', '%d')
        # self.etr_phone_number.bind("<Any-KeyPress>", self.validation_digit)
        self.etr_phone_number.bind("<Any-KeyRelease>", self.set_phone_number_form)
        self.etr_phone_number.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 우편물주소
        self.innerFrame08 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame08.pack(side='top', fill='x')

        self.lbl_post_address = Label(self.innerFrame08, text='우편물주소', width=10, font=12)
        self.lbl_post_address.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_post_address = StringVar()
        self.etr_post_address = Entry(self.innerFrame08, textvariable=self.text_post_address, relief='flat', font=12)
        self.etr_post_address.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 우편번호
        self.innerFrame09 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame09.pack(side='top', fill='x')

        self.lbl_post_number = Label(self.innerFrame09, text='우편번호', width=10, font=12)
        self.lbl_post_number.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_post_number = StringVar()
        self.etr_post_number = Entry(self.innerFrame09, textvariable=self.text_post_number, relief='flat', font=12)
        self.etr_post_number.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 전자우편
        self.innerFrame10 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame10.pack(side='top', fill='x')

        self.lbl_e_mail = Label(self.innerFrame10, text='전자우편', width=10, font=12)
        self.lbl_e_mail.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_e_mail = StringVar()
        self.etr_e_mail = Entry(self.innerFrame10, textvariable=self.text_e_mail, relief='flat', font=12)
        self.etr_e_mail.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 비고
        self.innerFrame11 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame11.pack(side='top', fill='x')

        self.lbl_csn_remark = Label(self.innerFrame11, text='비고', width=10, font=12)
        self.lbl_csn_remark.pack(side='left', ipady=2, fill='x', padx=1, pady=1)
        self.text_csn_remark = StringVar()
        self.etr_csn_remark = Entry(self.innerFrame11, textvariable=self.text_csn_remark, relief='flat', font=12)
        self.etr_csn_remark.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

    def get(self):
        widget_values = (int(self.etr_consignorID.get()),
                         self.etr_consignor.get(),
                         self.etr_business_number.get(),
                         self.etr_business_name.get(),
                         self.etr_owner_name.get(),
                         self.etr_business_state.get(),
                         self.etr_business_sector.get(),
                         self.etr_business_address.get(),
                         self.etr_phone_number.get(),
                         self.etr_post_number.get(),
                         self.etr_post_address.get(),
                         self.etr_e_mail.get(),
                         '',
                         self.etr_csn_remark.get())
        result = dict(zip(self.csnColumns, widget_values))
        return result

    def set(self, csn_dict):
        print('Run "class ConsignorInfo.set()"')
        if csn_dict['우편물주소'] != '':
            csn_dict['우편번호'] = PandasMod.correct_post_number_type(csn_dict['우편번호'])

        print(csn_dict)
        # for key in ocr_dict:
        #     print(f'{key}: {ocr_dict[key]}')
        # self.text_consignorID.set(ocr_dict['번호'])
        self.text_consignor.set(csn_dict['화주명'])
        self.text_business_number.set(csn_dict['사업자번호'])
        self.text_business_name.set(csn_dict['상호'])
        self.text_owner_name.set(csn_dict['대표자명'])
        self.text_business_state.set(csn_dict['업태'])
        self.text_business_sector.set(csn_dict['업종'])
        self.text_business_address.set(csn_dict['사업장주소'])
        self.text_phone_number.set(csn_dict['연락처'])
        self.text_post_address.set(csn_dict['우편물주소'])
        self.text_post_number.set(csn_dict['우편번호'])
        self.text_e_mail.set(csn_dict['전자우편'])
        if '비고' in csn_dict.keys():
            self.text_csn_remark.set(csn_dict['비고'])
        else:
            self.text_csn_remark.set('')
        if '화주ID' in csn_dict.keys():
            self.text_consignorID.set(csn_dict['화주ID'])
        else:
            self.set_consignor_id()

    def set_consignor_id(self):
        print('Run <set_consignor_id()>')
        csn_name = self.etr_consignor.get()
        same_csn_dict = PandasMod.get_same_csn(csn_name)
        self.master.master.consignorTreeview.update_csn_treeview(same_csn_dict)

        if len(same_csn_dict) == 1:
            print(f'same_csn_dict : \n {same_csn_dict}')
            same_csn_dict = same_csn_dict[list(same_csn_dict.keys())[0]].copy()
            self.text_consignorID.set(same_csn_dict['화주ID'])
            # self.master.master.csnTreeviewInfo.reset()
            self.master.master.csnTreeviewInfo.set(same_csn_dict)
        elif len(same_csn_dict) > 1:
            self.master.master.csnTreeviewInfo.reset()
        else:
            self.text_consignorID.set(ExcelMod.get_new_id('운송사목록'))
        print('Done <set_consignor_id()>')

    def set_consignor_id_by_event(self, event):
        self.set_consignor_id()

    def reset(self):
        self.text_consignorID.set('')
        self.text_consignor.set('')
        self.text_business_number.set('')
        self.text_business_name.set('')
        self.text_owner_name.set('')
        self.text_business_state.set('')
        self.text_business_sector.set('')
        self.text_business_address.set('')
        self.text_phone_number.set('')
        self.text_post_address.set('')
        self.text_post_number.set('')
        self.text_e_mail.set('')
        self.text_csn_remark.set('')

    def get_widgets(self):
        widgets = (self.etr_consignorID,
                   self.etr_consignor,
                   self.etr_business_number,
                   self.etr_business_name,
                   self.etr_owner_name,
                   self.etr_business_state,
                   self.etr_business_sector,
                   self.etr_business_address,
                   self.etr_phone_number,
                   self.etr_post_address,
                   self.etr_post_number,
                   self.etr_e_mail,
                   self.etr_csn_remark)
        return widgets

    def set_etr_business_number(self, event):
        if 5 > len(self.etr_business_number.get()) >= 4:
            if self.etr_business_number.get()[-1] != '-':
                self.etr_business_number.insert(3, '-')
                self.etr_business_number.icursor(END)
        if 7 > len(self.etr_business_number.get()) >= 6:
            if self.etr_business_number.get()[-1] != '-':
                self.etr_business_number.insert(6, '-')
                self.etr_business_number.icursor(END)

    def set_phone_number_form(self, envet):
        if len(self.etr_phone_number.get()) > 0:
            if self.etr_phone_number.get()[0] == '0':
                # 02-###-#####
                if self.etr_phone_number.get()[:2] == '02':
                    if 5 > len(self.etr_phone_number.get()) >= 3:
                        if self.etr_phone_number.get()[2] != '-':
                            self.etr_phone_number.insert(2, '-')
                            self.etr_phone_number.icursor(END)
                    if 12 > len(self.etr_phone_number.get()) >= 7:
                        if self.etr_phone_number.get()[6] != '-':
                            self.etr_phone_number.insert(6, '-')
                            self.etr_phone_number.icursor(END)
                    # 02-####-####
                    if len(self.etr_phone_number.get()) == 12:
                        if self.etr_phone_number.get()[8] != '-':
                            self.etr_phone_number.insert(8, '-')
                            self.etr_phone_number.delete(6, 7)
                            self.etr_phone_number.icursor(END)
                # 010-####-####, 070-####-####
                elif self.etr_phone_number.get()[:3] == ('010' or '070'):
                    if 5 > len(self.etr_phone_number.get()) >= 4:
                        if self.etr_phone_number.get()[3] != '-':
                            self.etr_phone_number.insert(3, '-')
                            self.etr_phone_number.icursor(END)
                    if 14 > len(self.etr_phone_number.get()) >= 9:
                        if self.etr_phone_number.get()[8] != '-':
                            self.etr_phone_number.insert(8, '-')
                            self.etr_phone_number.icursor(END)
                            # 031-###-####
                elif self.etr_phone_number.get()[:2] == ('03' or '04' or '05' or '06'):
                    if 5 > len(self.etr_phone_number.get()) >= 4:
                        if self.etr_phone_number.get()[3] != '-':
                            self.etr_phone_number.insert(3, '-')
                            self.etr_phone_number.icursor(END)
                    if 13 > len(self.etr_phone_number.get()) >= 8:
                        if self.etr_phone_number.get()[7] != '-':
                            self.etr_phone_number.insert(7, '-')
                            self.etr_phone_number.icursor(END)
            # 15##-####
            else:
                if 10 > len(self.etr_phone_number.get()) >= 5:
                    if self.etr_phone_number.get()[4] != '-':
                        self.etr_phone_number.insert(4, '-')
                        self.etr_phone_number.icursor(END)


if __name__ == '__main__':
    app = Tk()
    freight_info = ConsignorInfo(app)
    freight_info.config(text='화주정보')
    freight_info.pack()

    app.mainloop()
