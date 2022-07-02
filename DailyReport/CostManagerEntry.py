from tkinter import *
import tkinter.ttk as ttk
from datetime import datetime
import PandasMod


class CostManagerEntry(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # 날짜
        self.frame_date = Frame(self)
        self.frame_date.pack(expand=True, fill='x')

        self.lbl_date = Label(self.frame_date, text='날짜', relief='groove', width=10, height=1)
        self.lbl_date.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_date = StringVar()
        self.etr_date = Entry(self.frame_date, textvariable=self.text_date)
        self.etr_date.bind('<FocusOut>', self.transform_date)
        self.etr_date.pack(side='right', expand=True, fill='x', padx=3, pady=3, ipady=3)
        self.etr_date.focus()

        # 분류(콤보박스)
        self.frm_sector = Frame(self)
        self.frm_sector.pack(expand=True, fill='x')

        self.lbl_sector = Label(self.frm_sector, text='구분', relief='groove', width=10, height=1)
        self.lbl_sector.pack(side='left', padx=3, pady=3, ipady=3)

        cbo_sector_opt = ['연료', '정비', '우편', '주차', '대출', '24시', '용품', '이화', '고속도로', '벌금', '세금', '기타']
        self.text_cbo_sector = StringVar()
        self.cbo_sector = ttk.Combobox(self.frm_sector, textvariable=self.text_cbo_sector,
                                       values=cbo_sector_opt)  # , postcommand=self.set_cbo_item_opt)
        self.cbo_sector.bind('<FocusOut>', self.set_cbo_item_opt)
        self.cbo_sector.pack(side='right', expand=True, fill='x', padx=3, pady=3, ipady=3)

        # 항목(콤보박스)
        self.frm_item = Frame(self)
        self.frm_item.pack(expand=True, fill='x')

        self.lbl_item = Label(self.frm_item, text='항목', relief='groove', width=10, height=1)
        self.lbl_item.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_cbo_item = StringVar()
        self.cbo_item = ttk.Combobox(self.frm_item, textvariable=self.text_cbo_item)
        self.cbo_item.bind("<FocusOut>", self.config_etr_unit_and_qty)
        self.cbo_item.pack(side='right', expand=True, fill='x', padx=3, pady=3, ipady=3)

        # 금액
        self.frm_item_cost = Frame(self)
        self.frm_item_cost.pack(expand=True, fill='x')

        self.lbl_item_cost = Label(self.frm_item_cost, text='비용', relief='groove', width=10, height=1)
        self.lbl_item_cost.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_item_cost = StringVar()
        self.etr_item_cost = Entry(self.frm_item_cost, validate="key", justify=RIGHT, textvariable=self.text_item_cost)
        self.etr_item_cost['validatecommand'] = (self.etr_item_cost.register(testval), '%P', '%d')
        self.etr_item_cost.bind("<Any-KeyRelease>", self.set_item_cost_form)
        self.etr_item_cost.bind("<FocusOut>", self.config_etr_unit_and_qty)
        self.etr_item_cost.pack(side='right', expand=True, fill='x', padx=3, pady=3, ipady=3)

        # 단가, 수량
        self.frm_unit_price_and_qty = Frame(self)
        self.frm_unit_price_and_qty.pack(expand=True, fill='x')

        self.lbl_unit_price = Label(self.frm_unit_price_and_qty, text='단가', relief='groove', width=10, height=1)
        self.lbl_unit_price.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_unit_price = StringVar()
        self.etr_unit_price = Entry(self.frm_unit_price_and_qty, validate="key", justify=RIGHT,
                                    textvariable=self.text_unit_price, takefocus=False)
        self.etr_unit_price['validatecommand'] = (self.etr_item_cost.register(testval), '%P', '%d')
        self.etr_unit_price.bind("<Any-KeyRelease>", self.set_unit_cost_form)

        self.etr_unit_price.pack(side='left', expand=True, fill='x', padx=3, pady=3, ipady=3)

        self.lbl_quantity = Label(self.frm_unit_price_and_qty, text='수량', relief='groove', width=10, height=1)
        self.lbl_quantity.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_quantity = StringVar()
        self.etr_quantity = Entry(self.frm_unit_price_and_qty, validate="key", justify=RIGHT,
                                  textvariable=self.text_quantity, takefocus=False)
        self.etr_quantity['validatecommand'] = (self.etr_item_cost.register(testval), '%P', '%d')
        self.etr_quantity.pack(side='left', expand=True, fill='x', padx=3, pady=3, ipady=3)

        # 운행거리
        self.frm_mileage = Frame(self)
        self.frm_mileage.pack(expand=True, fill='x')

        self.lbl_mileage = Label(self.frm_mileage, text='운행거리', relief='groove', width=10, height=1)
        self.lbl_mileage.pack(side='left', padx=3, pady=3, ipady=3)

        self.text_mileage = StringVar()
        self.etr_mileage = Entry(self.frm_mileage, justify=RIGHT, validate="key", textvariable=self.text_mileage)
        self.etr_mileage['validatecommand'] = (self.etr_item_cost.register(testval), '%P', '%d')
        self.etr_mileage.bind("<Any-KeyRelease>", self.set_mileage_form)
        self.etr_mileage.bind("<Return>", self.focus_input_btn)

        self.etr_mileage.pack(side='right', expand=True, fill='x', padx=3, pady=3, ipady=3)

    def transform_date(self, event):
        if self.text_date.get() != '':
            date_now = datetime.now().month
            input_month = datetime.strptime(self.etr_date.get(), '%m/%d').month
            if input_month > date_now > 12:
                str_year = datetime.now().year - 1
            else:
                str_year = datetime.now().year
            self.text_date.set(f'{str_year}/{self.etr_date.get()}')

    def set_cbo_item_opt(self, event):
        if self.cbo_sector.get() == '정비':
            cbo_item_opt = ['엔진오일', '타이어', '에어필터', 'CCV필터', '수리', '기타']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '연료':
            cbo_item_opt = ['디젤', '요소수']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '24시':
            cbo_item_opt = ['수수료']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '고속도로':
            cbo_item_opt = ['통행료']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '대출':
            cbo_item_opt = ['현대카드', '신한카드', '국민카드', '농협캐피탈', '햇살론', '웰컴저축은행', '현대캐피탈', ]
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '우편':
            cbo_item_opt = ['우편']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '주차':
            cbo_item_opt = ['주차']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '용품':
            cbo_item_opt = ['램프', '공구', '와이퍼']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '이화':
            cbo_item_opt = ['관리비', '화물보험']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '벌금':
            cbo_item_opt = ['과속', '주차', '밤샘주자', '신호위반', '기타']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '세금':
            cbo_item_opt = ['부가세', '소득세', '종합소득세', '기타']
            self.cbo_item.config(values=cbo_item_opt)
        elif self.cbo_sector.get() == '기타':
            cbo_item_opt = ['기타']
            self.cbo_item.config(values=cbo_item_opt)
        else:
            cbo_item_opt = []
            self.cbo_item.config(values=cbo_item_opt)

    def config_etr_unit_and_qty(self, event):
        if self.cbo_item.get() == '디젤':
            self.etr_unit_price.config(takefocus=True)
            self.etr_quantity.config(takefocus=True)
        else:
            self.etr_unit_price.config(takefocus=False)
            self.etr_quantity.config(takefocus=False)

    def set_unit_cost_form(self, event):
        input_char = event.keysym
        if '￦ ' in self.etr_unit_price.get():
            show_text = self.etr_unit_price.get().replace(',', '').replace('￦ ', '')
        else:
            show_text = ''
        self.text_unit_price.set('')

        if input_char.isdigit():
            show_text = show_text + input_char
        if len(show_text) > 0:
            self.text_unit_price.set(PandasMod.translate_currency(int(show_text)))
        self.etr_unit_price.icursor(END)

    def set_item_cost_form(self, event):
        input_char = event.keysym
        if '￦ ' in self.etr_item_cost.get():
            show_text = self.etr_item_cost.get().replace(',', '').replace('￦ ', '')
        else:
            show_text = ''
        self.text_item_cost.set('')

        if input_char.isdigit():
            show_text = show_text + input_char
        if len(show_text) > 0:
            self.text_item_cost.set(PandasMod.translate_currency(int(show_text)))
        self.etr_item_cost.icursor(END)

    def set_mileage_form(self, event):
        input_char = event.keysym
        if ' ㎞' in self.etr_mileage.get():
            show_text = self.etr_mileage.get().replace(',', '').replace(' ㎞', '')
        else:
            show_text = ''
        self.text_mileage.set('')

        if input_char.isdigit():
            show_text = show_text + event.keysym
        if len(show_text) > 0:
            self.text_mileage.set(str(PandasMod.group(int(show_text))) + ' ㎞')
        idx = self.etr_mileage.index(END)
        self.etr_mileage.icursor(idx - 2)

    def focus_input_btn(self):
        self.master.master.btn_input.focus()

    def get(self):
        etr_keys = ('날짜', '분류', '항목', '금액', '단가', '수량', '운행거리', '비고')
        date = datetime.strptime(self.etr_date.get(), '%Y/%m/%d').date()
        item_cost = PandasMod.currency_to_int(self.etr_item_cost.get())
        if self.etr_unit_price.get() != '':
            unit_cost = PandasMod.currency_to_int(self.etr_unit_price.get())
        else:
            unit_cost = ''
        if self.etr_mileage.get() != '':
            mileage = PandasMod.mileage_to_int(self.etr_mileage.get())
        else:
            mileage = ''
        if self.etr_quantity.get() != '':
            quantity = int(self.etr_quantity.get())
        else:
            quantity = ''
        etr_values = (date, self.cbo_sector.get(), self.cbo_item.get(),
                      item_cost, unit_cost, quantity, mileage)

        result = dict(zip(etr_keys, etr_values))

        return result

    def set(self, cost_dict):
        self.text_date.set(cost_dict['날짜']),
        self.text_cbo_sector.set(cost_dict['분류']),
        self.text_cbo_item.set(cost_dict['항목']),
        self.text_item_cost.set(cost_dict['금액']),
        self.text_unit_price.set(cost_dict['단가']),
        self.text_quantity.set(cost_dict['수량']),
        self.text_mileage.set(cost_dict['운행거리']),
    
    def reset(self):
        self.text_date.set('')
        self.text_cbo_sector.set('')
        self.text_cbo_item.set('')
        self.text_item_cost.set('')
        self.text_unit_price.set('')
        self.text_quantity.set('')
        self.text_mileage.set('')
        self.etr_date.focus()


def testval(instr, acttyp):
    if acttyp == '1':  # insert
        if not instr.isdigit():
            return False
    return True


if __name__ == '__main__':
    app = Tk()
    app_widget = CostManagerEntry(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
