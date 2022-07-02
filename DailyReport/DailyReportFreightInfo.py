from tkinter import *
import tkinter.font
import tkinter.ttk as ttk
import ExcelMod
from datetime import datetime
import PandasMod


class FreightInfo(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)
        self.keys = ('일보ID', '배차시간', '화물번호', '상차지', '하차지', '화주ID', '화주명', '거리', '상하차일',
                     '상하차방법', '화물정보', '혼적', '수량', '단위', '톤수', '차종', '적재중량', '운행방법', '비고')  # 19

        self.frm_lbl_freight_id_title = Frame(self)
        self.frm_lbl_freight_id_title.pack(side='top', expand=True, fill='x')
        # self.frm_lbl_freight_id_title.pack(padx=1, pady=1, ipady=3, fill='x')row=0, column=0, columnspan=4,
        #                                    sticky='nw'+'ne'+'sw'+'se')

        # 운행일보 번호(ID)
        self.text_freight_id = StringVar()
        self.text_freight_id.set(str(0))  # ExcelMod.get_new_id('운행일보')))

        self.lbl_freight_id_title = Label(self.frm_lbl_freight_id_title, text='번호 : ', font=12)
        self.lbl_freight_id_title.pack(side='left', expand=True, anchor='e')

        self.etr_freight_id = Entry(self.frm_lbl_freight_id_title, textvariable=self.text_freight_id,
                                    font=12, bd=0, bg='whitesmoke', width=0, justify='right')
        self.etr_freight_id.pack(side='left', anchor='e', padx=1, pady=2)

        # 바깥 테두리
        self.out_frm = Frame(self, bg='#AAAAAA')
        self.out_frm.pack(side='top', anchor='n', fill='both', padx=5, pady=5)

        self.inner_frm = Frame(self.out_frm, bg='#AAAAAA')
        self.inner_frm.pack(side='top', anchor='n', fill='both', padx=1, pady=1)

        # 배차시간
        self.inner_frm01 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm01.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_load_date = Label(self.inner_frm01, text='배차시간', relief='flat', width=9, font=12)
        self.lbl_load_date.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_load_date = StringVar()
        self.etr_load_date = Entry(self.inner_frm01, textvariable=self.text_load_date, relief='flat', font=12, width=0)
        self.etr_load_date.pack(side='right', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 화물번호
        self.inner_frm02 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm02.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_freight_number = Label(self.inner_frm02, text='화물번호', relief='flat', width=9, font=12)
        self.lbl_freight_number.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_freight_number = StringVar()
        self.etr_freight_number = Entry(self.inner_frm02, textvariable=self.text_freight_number, relief='flat', font=12)
        self.etr_freight_number.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 상차지
        self.inner_frm03 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm03.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_load_location = Label(self.inner_frm03, text='상차지', relief='flat', width=9, font=12)
        self.lbl_load_location.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_load_location = StringVar()
        self.etr_load_location = Entry(self.inner_frm03, textvariable=self.text_load_location, relief='flat', font=12)
        self.etr_load_location.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 하차지
        self.inner_frm04 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm04.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_unload_location = Label(self.inner_frm04, text='하차지', relief='flat', width=9, font=12)
        self.lbl_unload_location.pack(side='left', padx=1, pady=1, ipady=2, fill='both')

        # 하차지 엔트리 프레임
        self.frm_etr_unload_location = Frame(self.inner_frm04)
        self.frm_etr_unload_location.pack(side='left', padx=1, pady=1, fill='x', expand=True)

        # 하차지 엔트리
        self.text_unload_location = StringVar()
        self.etr_unload_location = Entry(self.frm_etr_unload_location, textvariable=self.text_unload_location,
                                         relief='flat', width=9, font=12)
        self.etr_unload_location.pack(side='top', fill='x', expand=True, ipady=3)

        # 거리
        self.fi_font = tkinter.font.Font(size=12, slant='italic')
        self.text_distance = StringVar()
        self.etr_distance = Entry(self.frm_etr_unload_location, textvariable=self.text_distance,
                                  relief='flat', justify='center', font=self.fi_font, width=6)
        self.etr_distance.pack(side='left', expand=True, fill='x', ipady=3)

        # 상하차일
        self.text_load_day = StringVar()
        self.etr_load_day = Entry(self.frm_etr_unload_location, textvariable=self.text_load_day,
                                  relief='flat', justify='center', font=self.fi_font, width=6)
        self.etr_load_day.pack(side='left', expand=True, fill='x', ipady=3)

        # 상하차방법
        self.text_load_method = StringVar()
        self.etr_load_method = Entry(self.frm_etr_unload_location, textvariable=self.text_load_method,
                                     relief='flat', justify='center', font=self.fi_font, width=6)
        self.etr_load_method.pack(side='left', expand=True, fill='x', ipady=3)

        # 운송사
        self.inner_frm05 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm05.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_dr_consignor = Label(self.inner_frm05, text='화주명', relief='flat', width=9, font=12)
        self.lbl_dr_consignor.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_dr_consignor = StringVar()
        self.etr_dr_consignor = Entry(self.inner_frm05, textvariable=self.text_dr_consignor, relief='flat', font=12)
        self.etr_dr_consignor.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)
        self.etr_dr_consignor.bind('<FocusOut>', self.update_csn_list)
        # self.etr_dr_consignor.bind('<Tab>', self.go_next_entry)

        # 화물정보
        self.inner_frm06 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm06.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_freight_info = Label(self.inner_frm06, text='화물정보', relief='flat', width=9, font=12)
        self.lbl_freight_info.pack(side='left', padx=1, pady=1, ipady=2, fill='both')

        self.txt_freight_info = Text(self.inner_frm06, relief='flat', font=12, width=40, height=3, spacing2=3,
                                     wrap='word')
        self.txt_freight_info.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 혼적
        self.inner_frm07 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm07.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_consoldation = Label(self.inner_frm07, text='혼적', relief='flat', width=9, font=12)
        self.lbl_consoldation.pack(side='left', padx=1, pady=1, ipady=3)

        self.text_consoldation = StringVar()
        self.etr_consoldation = Entry(self.inner_frm07, textvariable=self.text_consoldation, relief='flat',
                                      width=5, font=12)
        self.etr_consoldation.pack(side='left', expand=True, fill='x', ipady=4, padx=1)

        # 수량
        self.lbl_quantity = Label(self.inner_frm07, text='수량', relief='flat', width=9, font=12)
        self.lbl_quantity.pack(side='left', padx=1, pady=1, ipady=3)

        self.text_quantity = StringVar()
        self.etr_quantity = Entry(self.inner_frm07, textvariable=self.text_quantity, relief='flat',
                                  width=5, font=12)
        self.etr_quantity.pack(side='left', expand=True, fill='x', ipady=4, padx=1)

        # 단위
        self.lbl_unit = Label(self.inner_frm07, text='단위', relief='flat', width=9, font=12)
        self.lbl_unit.pack(side='left', padx=1, pady=1, ipady=3)

        cbo_unit_opt = ['P/T', 'M', 'CTN', 'CBM']
        self.text_unit = StringVar()
        self.cbo_unit = ttk.Combobox(self.inner_frm07, textvariable=self.text_unit,
                                     values=cbo_unit_opt, width=5, font=12)
        self.cbo_unit.pack(side='left', expand=True, fill='x', ipady=4, padx=1)

        # 톤수
        self.inner_frm08 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm08.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_truck_weight = Label(self.inner_frm08, text='톤수', relief='flat', width=9, font=12)
        self.lbl_truck_weight.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_truck_weight = StringVar()
        self.etr_truck_weight = Entry(self.inner_frm08, textvariable=self.text_truck_weight, relief='flat',
                                      width=15, font=12)
        self.etr_truck_weight.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 차종
        self.lbl_truck_type = Label(self.inner_frm08, text='차종', relief='flat', width=9, font=12)
        self.lbl_truck_type.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_truck_type = StringVar()
        self.etr_truck_type = Entry(self.inner_frm08, textvariable=self.text_truck_type, relief='flat',
                                    width=15, font=12)
        self.etr_truck_type.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 적재중량
        self.inner_frm09 = Frame(self.inner_frm, bg='#AAAAAA')
        self.inner_frm09.pack(side='top', anchor='n', fill='x')  # , padx=1, pady=1)

        self.lbl_load_weight = Label(self.inner_frm09, text='적재중량', relief='flat', width=9, font=12)
        self.lbl_load_weight.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_load_weight = StringVar()
        self.etr_load_weight = Entry(self.inner_frm09, textvariable=self.text_load_weight, relief='flat',
                                     width=15, font=12)
        self.etr_load_weight.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

        # 운행방법
        self.lbl_how_to_operator = Label(self.inner_frm09, text='운행방법', relief='flat', width=9, font=12)
        self.lbl_how_to_operator.pack(side='left', padx=1, pady=1, ipady=2, fill='x')

        self.text_how_to_operator = StringVar()
        self.etr_how_to_operator = Entry(self.inner_frm09, textvariable=self.text_how_to_operator, relief='flat',
                                         width=15, font=12)
        self.etr_how_to_operator.pack(side='left', padx=1, pady=1, ipady=3, fill='x', expand=True)

    def update_csn_list(self, event):
        csn_name = self.etr_dr_consignor.get()
        self.master.master.consignorTreeview.update_csn_same_list(csn_name)

    def get(self):
        if self.etr_quantity.get() != '':
            quantity = int(self.etr_quantity.get())
        else:
            quantity = ''
        widget_values = (int(self.etr_freight_id.get()),
                         datetime.strptime(self.etr_load_date.get(), '%Y-%m-%d %H:%M').date(),
                         self.etr_freight_number.get(),
                         self.etr_load_location.get(),
                         self.etr_unload_location.get(),
                         int(self.master.master.consignorInfo.etr_consignorID.get()),
                         self.etr_dr_consignor.get(),
                         PandasMod.mileage_to_int(self.etr_distance.get()),
                         self.etr_load_day.get(),
                         self.etr_load_method.get(),
                         self.txt_freight_info.get(1.0, END).strip('\n'),
                         self.etr_consoldation.get(),
                         quantity,
                         self.cbo_unit.get(),
                         self.etr_truck_weight.get(),
                         self.etr_truck_type.get(),
                         self.etr_load_weight.get(),
                         self.etr_how_to_operator.get(),
                         '')

        result = dict(zip(self.keys, widget_values))

        return result

    def set(self, freight_dict):
        self.text_load_date.set(freight_dict['배차시간'])
        self.text_freight_number.set(freight_dict['화물번호'])
        self.text_load_location.set(freight_dict['상차지'])
        self.text_unload_location.set(freight_dict['하차지'])
        self.text_distance.set(str(freight_dict['거리'])+' ㎞')
        self.text_load_day.set(freight_dict['상하차일'])
        self.text_load_method.set(freight_dict['상하차방법'])
        self.text_dr_consignor.set(freight_dict['화주명'])
        self.txt_freight_info.insert(1.0, freight_dict['화물정보'])
        self.text_consoldation.set(freight_dict['혼적'])
        if freight_dict['수량'] is None:
            self.text_quantity.set('')
        else:
            self.text_quantity.set(freight_dict['수량'])
        if freight_dict['단위'] is None:
            self.text_unit.set('')
        else:
            self.text_unit.set(freight_dict['단위'])
        self.text_truck_weight.set(freight_dict['톤수'])
        self.text_truck_type.set(freight_dict['차종'])
        self.text_load_weight.set(freight_dict['적재중량'])
        self.text_how_to_operator.set(freight_dict['운행방법'])
        if '일보ID' in freight_dict.keys():
            self.text_freight_id.set(freight_dict['일보ID'])
        else:
            self.text_freight_id.set(ExcelMod.get_new_id('운행일보'))

    def get_widgets(self):
        widgets = (self.etr_freight_id,
                   self.etr_load_date,
                   self.etr_freight_number,
                   self.etr_load_location,
                   self.etr_unload_location,
                   self.etr_distance,
                   self.etr_load_day,
                   self.etr_load_method,
                   self.etr_dr_consignor,
                   self.txt_freight_info,
                   self.etr_consoldation,
                   self.etr_quantity,
                   self.cbo_unit,
                   self.etr_truck_weight,
                   self.etr_truck_type,
                   self.etr_load_weight,
                   self.etr_how_to_operator)

        return widgets

    def get_widgets_variables(self):
        return (self.text_load_date,
                self.text_freight_number,
                self.text_load_location,
                self.text_unload_location,
                self.text_distance,
                self.text_load_day,
                self.text_load_method,
                self.text_dr_consignor,
                self.txt_freight_info,
                self.text_consoldation,
                self.text_quantity,
                self.text_unit,
                self.text_truck_weight,
                self.text_truck_type,
                self.text_load_weight,
                self.text_how_to_operator)

    def reset(self):
        self.text_load_date.set('')
        self.text_freight_number.set('')
        self.text_load_location.set('')
        self.text_unload_location.set('')
        self.text_distance.set('')
        self.text_load_day.set('')
        self.text_load_method.set('')
        self.text_dr_consignor.set('')
        self.txt_freight_info.delete(1.0, END)
        self.text_consoldation.set('')
        self.text_quantity.set('')
        self.text_unit.set('')
        self.text_truck_weight.set('')
        self.text_truck_type.set('')
        self.text_load_weight.set('')
        self.text_how_to_operator.set('')


if __name__ == '__main__':
    app = Tk()
    freight_info = FreightInfo(app)
    freight_info.config(text='화물정보')
    freight_info.pack()

    app.mainloop()
