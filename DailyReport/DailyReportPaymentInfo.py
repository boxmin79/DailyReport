from tkinter import *
import tkinter.ttk as ttk
from datetime import datetime

import pandas as pd

import PandasMod


class PaymentInfo(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.keys = ('일보ID', '배차시간', '화주ID', '화주명', '운송료', '수수료', '결제방법', '합계금액', '계산서', '발행방법',
                     '수금상태', '보낸분')  # 12

        self.out_frm = Frame(self, bg='#AAAAAA')
        self.out_frm.pack(side='top', expand=True, fill='both', padx=5, pady=5)

        self.innerFrame = Frame(self.out_frm, bg='#AAAAAA')
        self.innerFrame.pack(side='top', expand=True, fill='both', padx=1, pady=1)

        # 운송료
        self.innerFrame01 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame01.pack(side='top', fill='x')
        
        self.lbl_fare = Label(self.innerFrame01, text='운송료', width=9, height=1, relief='flat', font=12)
        self.lbl_fare.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_fare = StringVar()
        self.etr_fare = Entry(self.innerFrame01, textvariable=self.text_fare, relief='flat', width=15, font=12)
        self.etr_fare.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)
        # 수수료
        self.lbl_commission = Label(self.innerFrame01, text='수수료', width=9, height=1, relief='flat', font=12)
        self.lbl_commission.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_commission = StringVar()
        self.etr_commission = Entry(self.innerFrame01, textvariable=self.text_commission, relief='flat', width=15, font=12)
        self.etr_commission.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 결제방법
        self.innerFrame02 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame02.pack(side='top', fill='x')
        
        self.lbl_payment_method = Label(self.innerFrame02, text='결제방법', width=9, height=1, relief='flat', font=12)
        self.lbl_payment_method.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_payment_method = StringVar()
        self.etr_payment_method = Entry(self.innerFrame02, textvariable=self.text_payment_method, relief='flat',
                                        width=15, font=12)
        self.etr_payment_method.bind('<FocusOut>', self.set_payment_method)
        self.etr_payment_method.bind('<Return>', self.set_payment_method)
        self.etr_payment_method.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 합계금액
        self.lbl_total_fare = Label(self.innerFrame02, text='합계금액', width=9, height=1, relief='flat', font=12)
        self.lbl_total_fare.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_total_fare = StringVar()
        self.etr_total_fare = Entry(self.innerFrame02, textvariable=self.text_total_fare, relief='flat', width=15, font=12)
        self.etr_total_fare.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 세금계산서
        self.innerFrame03 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame03.pack(side='top', fill='x')
        
        self.lbl_issue_tax_invoice_state = Label(self.innerFrame03, text='세금계산서', width=9, height=1, relief='flat',
                                                 font=12)
        self.lbl_issue_tax_invoice_state.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_issue_tax_invoice_state = StringVar()
        self.etr_issue_tax_invoice_state = Entry(self.innerFrame03, textvariable=self.text_issue_tax_invoice_state,
                                                 relief='flat', width=15, font=12)

        self.etr_issue_tax_invoice_state.pack(side='left', expand=True, ipady=3, fill='x', padx=1, pady=1)

        # 발행방법
        self.lbl_issue_method = Label(self.innerFrame03, text='발행방법', width=9, height=1, relief='flat', font=12)
        self.lbl_issue_method.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        cbo_issue_method_opt = ['우편', '전자', '수기']
        self.text_issue_method = StringVar()
        self.cbo_issue_method = ttk.Combobox(self.innerFrame03, textvariable=self.text_issue_method,
                                             values=cbo_issue_method_opt, font=12, width=13)
        self.cbo_issue_method.bind('<<ComboboxSelected>>', self.set_issue_state)
        self.cbo_issue_method.pack(side='left', expand=True, ipady=3, fill='x')  # , padx=1, pady=1)

        # 수금상태
        self.innerFrame04 = Frame(self.innerFrame, bg='#AAAAAA')
        self.innerFrame04.pack(side='top', fill='x')
        
        self.lbl_collect_state = Label(self.innerFrame04, text='수금상태', width=9, height=1, relief='flat', font=12)
        self.lbl_collect_state.pack(side='left', ipady=2, fill='x', padx=1, pady=1)

        self.text_collect_state = StringVar()
        self.etr_collect_state = Entry(self.innerFrame04, textvariable=self.text_collect_state, relief='flat', font=12)

        self.etr_collect_state.pack(side='right', expand=True, ipady=3, fill='x', padx=1, pady=1)

    def set_payment_method(self, event):
        if self.etr_payment_method.get() == '인수증':
            self.text_issue_tax_invoice_state.set('')
            self.text_issue_method.set('우편')

    def get_widgets(self):
        widgets = (self.etr_fare,
                   self.etr_commission,
                   self.etr_payment_method,
                   self.etr_total_fare,
                   self.etr_issue_tax_invoice_state,
                   self.cbo_issue_method,
                   self.etr_collect_state)

        return widgets

    def get(self):
        print('Run <PaymentInfo.get()>')
        if self.etr_issue_tax_invoice_state.get() != '':
            invoice_state = datetime.strptime(self.etr_issue_tax_invoice_state.get(), '%Y-%m-%d %H:%M').date()
        else:
            invoice_state = self.etr_issue_tax_invoice_state.get()
        load_date = datetime.strptime(self.master.master.freightInfo.etr_load_date.get(), '%Y-%m-%d %H:%M').date()
        if self.etr_collect_state.get() != '':
            collect_state = datetime.strptime(self.etr_collect_state.get(), '%Y-%m-%d %H:%M').date()
        else:
            collect_state = self.etr_collect_state.get()
        widgets_values = (int(self.master.master.freightInfo.etr_freight_id.get()),
                          load_date,
                          int(self.master.master.consignorInfo.etr_consignorID.get()),
                          self.master.master.consignorInfo.etr_consignor.get(),
                          PandasMod.currency_to_int(self.etr_fare.get()),
                          PandasMod.currency_to_int(self.etr_commission.get()),
                          self.etr_payment_method.get(),
                          PandasMod.currency_to_int(self.etr_total_fare.get()),
                          invoice_state,
                          self.cbo_issue_method.get(),
                          collect_state,
                          '')
        result = dict(zip(self.keys, widgets_values))
        print('return result')
        print('Run <PaymentInfo.get()>')
        return result

    def set(self, pay_dict):
        print('Run <PaymentInfo.set()>')
        for idx in pay_dict:
            print(f'{idx}: {pay_dict[idx]}')
        print('=============')
        self.text_fare.set(pay_dict['운송료'])
        self.text_commission.set(pay_dict['수수료'])
        self.text_payment_method.set(pay_dict['결제방법'])
        self.text_total_fare.set(pay_dict['합계금액'])

        if pay_dict['전자세금계산서'] == '미발행상태':
            if pay_dict['계산서'] == '미발행':
                self.text_issue_tax_invoice_state.set('')
            else:
                self.text_issue_tax_invoice_state.set(pay_dict['계산서'])
        elif pay_dict['전자세금계산서'] == '전자발행':
            self.text_issue_tax_invoice_state.set(self.master.master.freightInfo.etr_load_date.get())
        else:
            self.text_issue_tax_invoice_state.set(pay_dict['계산서'])

        print(f"\n=========================================\n"
              f"pay_dict['수금상태'] : {pay_dict['수금상태']}\n>"
              f"type : {type(pay_dict['수금상태'])}"
              f"\n=========================================\n")

        if str(type(pay_dict['수금상태'])) == "<class 'pandas._libs.tslibs.nattype.NaTType'>":
            if pay_dict['수금상태'] == pd.NaT:
                print(f"pay_dict['수금상태'] : {pay_dict['수금상태']}\n>")
                collect_str = ''
            else:
                collect_str = pay_dict['수금상태']
        elif str(type(pay_dict['수금상태'])) == "<class 'str'>":
                if pay_dict['수금상태'] == '<미수금>':
                    collect_str = ''
                elif ('가상계좌정산' or '카드승인') in pay_dict['수금상태']:
                    collect_str = pay_dict['수금상태'][-19:-3]
        else:
            collect_str = pay_dict['수금상태']

        self.text_collect_state.set(collect_str)

        if '발행방법' in list(pay_dict.keys()):
            self.text_issue_method.set(pay_dict['발행방법'])
        else:
            self.set_issue_method()
        print('Done <PaymentInfo.set()>')

    def set_issue_state(self, event):
        print('Run <PaymentInfo.set_issue_state()')
        print(f'self.cbo_issue_method.get() : {self.cbo_issue_method.get()}')
        if self.cbo_issue_method.get() == '전자':
            self.text_issue_tax_invoice_state.set(self.master.master.freightInfo.etr_load_date.get())
        print('Done <PaymentInfo.set_issue_state()')

    def set_issue_method(self):
        print('<PaymentInfo.set_issue_method()> 실행')
        if self.etr_payment_method.get() == '인수증':
            # print('발행방법 = 인수증')
            if self.etr_issue_tax_invoice_state.get() == '':
                # print('계산서 : 미발행')
                self.text_issue_method.set('우편')
            else:
                self.text_issue_method.set('전자')
        elif self.etr_payment_method.get() == '선/착불':
            self.text_issue_method.set('수기')
        elif self.etr_payment_method.get() == '카드':
            self.text_issue_method.set('전자')
        print('<PaymentInfo.set_issue_method()> 종료')

    def reset(self):
        self.text_fare.set('')
        self.text_commission.set('')
        self.text_payment_method.set('')
        self.text_total_fare.set('')
        self.text_issue_tax_invoice_state.set('')
        self.text_collect_state.set('')
        self.text_issue_method.set('')


if __name__ == '__main__':
    app = Tk()
    freight_info = PaymentInfo(app)
    freight_info.config(text='결제정보')
    freight_info.pack(side='top', fill='x')

    app.mainloop()
