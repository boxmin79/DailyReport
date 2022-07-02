from tkinter import *
import PandasMod


class ConsignorTreeviewInfo(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.csn_dict = {'화주ID': '', '화주명': '', '사업자번호': '', '상호': '',
                         '대표': '', '업태': '', '종목': '', '사업장주소': '',
                         '전화번호': '', '우편번호': '', '우편주소': '', '이메일': '',
                         '전화번호2': '', '비고': ''}

        self.txt_message = Text(self, bg='whitesmoke', bd=0, width=0, wrap='word', spacing1=5, spacing2=5, spacing3=5)
        self.txt_message.pack(side='top', fill='x', anchor='nw',
                              ipadx=10, ipady=10, padx=10, pady=3)

        self.set(self.csn_dict)

    def reset(self):
        self.set(self.csn_dict)

    def clear(self):
        self.txt_message.delete(1.0, END)

    def set(self, csn_dict):
        print('Run <ConsignorTreeviewInfo.set()>')
        print(f'csn_dict : \n type: {type(csn_dict)} \n {csn_dict}')

        csn_dict['우편번호'] = PandasMod.correct_post_number_type(csn_dict['우편번호'])
        self.clear()
        for idx in csn_dict:
            self.txt_message.insert(END, f'{idx} : {csn_dict[idx]}\n')
        print('Done <ConsignorTreeviewInfo.set()>')


if __name__ == '__main__':
    app = Tk()
    freight_info = ConsignorTreeviewInfo(app)
    freight_info.config()
    freight_info.pack()

    app.mainloop()
