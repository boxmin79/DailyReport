from tkinter import *
import PandasMod


class DailyReportTreeviewInfo(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.dr_dict = {'일보ID': '', '배차시간': '', '화물번호': '', '상차지': '', '하차지': '', '화주ID': '',
                        '화주명': '', '거리': '', '상하차일': '', '상하차방법': '', '화물정보': '', '혼적': '',
                        '수량': '', '단위': '', '톤수': '', '차종': '', '적재중량': '', '운행방법': '', '비고': '',
                        '운임': '', '수수료': '', '결제방법': '', '합계금액': '',
                        '발행일': '', '발행방법': '', '입금일': '', '보낸분': ''}

        self.txt_message = Text(self, bg='whitesmoke', bd=0, width=0, wrap='word', spacing1=5)
        self.txt_message.pack(side='top', expand=True, fill='both',
                              ipadx=10, ipady=10, padx=10, pady=3)

        self.set(self.dr_dict)

    def reset(self):
        self.set(self.dr_dict)

    def clear(self):
        self.txt_message.delete(1.0, END)

    def set(self, dr_dict):
        self.clear()
        for idx in dr_dict:
            self.txt_message.insert(END, f'{idx} : {dr_dict[idx]}\n')


if __name__ == '__main__':
    app = Tk()
    app_widget = DailyReportTreeviewInfo(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
