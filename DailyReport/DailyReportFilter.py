from datetime import datetime
from tkinter import *
import PILMod
import DailyReportCalendar
from tkinter import messagebox
import PandasMod


class DailyReportFilter(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.cal_icon_file = 'C:/Users/realb/PycharmProjects/DailyReport/Icon/calendar.png'
        self.cal_img = PILMod.get_icon_img(self.cal_icon_file, 25, 25)

        self.what_day = None

        # 3. 조회버튼
        self.btn_Lookup = Button(self, text='조회', bg='gray', width=6, font=12,
                                 command=self.call_dr_filter)
        self.btn_Lookup.pack(side='right', fill='both', anchor=CENTER,
                             padx=5, pady=5)

        # 1.날짜
        self.frm_lookup_date = Frame(self)
        self.frm_lookup_date.pack(side='top', expand=True, fill='x', padx=3, pady=3)

        # 1-1 검색 시작일 엔트리
        self.lbl_start_date = Label(self.frm_lookup_date, text='시작', font=12)
        self.lbl_start_date.pack(side='left')

        self.text_start_date = StringVar()
        self.etr_start_date = Entry(self.frm_lookup_date, textvariable=self.text_start_date, font=12, width=10)
        self.etr_start_date.pack(side='left', expand=True, fill='x', ipady=3)

        self.btn_start_date = Button(self.frm_lookup_date, command=lambda: self.call_calendar('start'),
                                     image=self.cal_img, bd=0)
        self.btn_start_date.pack(side='left', anchor=CENTER, padx=3, pady=3)

        self.lbl_wave_mark = Label(self.frm_lookup_date, text='~', font=12)
        self.lbl_wave_mark.pack(side='left')
        # 2-2 검색 종료일 엔트리
        self.lbl_end_date = Label(self.frm_lookup_date, text='종료', font=12)
        self.lbl_end_date.pack(side='left')

        self.text_end_date = StringVar()
        self.etr_end_date = Entry(self.frm_lookup_date, textvariable=self.text_end_date, font=12, width=10)
        self.etr_end_date.pack(side='left', expand=True, fill='x', ipady=3)

        self.btn_end_date = Button(self.frm_lookup_date, command=lambda: self.call_calendar('end'),
                                   image=self.cal_img, bd=0)
        self.btn_end_date.pack(side='left', padx=3, pady=3)

        # 2. 전체, 수금, 미수금
        self.frm_check_button = Frame(self)
        self.frm_check_button.pack(side='top', anchor='w')

        self.filter_option = IntVar()

        self.radioAll = Radiobutton(self.frm_check_button, text="전체", value=0, variable=self.filter_option)
        self.radioDeposit = Radiobutton(self.frm_check_button, text="수금", value=1, variable=self.filter_option)
        self.radioReceivable = Radiobutton(self.frm_check_button, text="미수금", value=2, variable=self.filter_option)

        self.radioAll.pack(side='left')
        self.radioDeposit.pack(side='left')
        self.radioReceivable.pack(side='left')

    def call_dr_filter(self):

        # 1. 날짜 입력 검사
        if self.etr_start_date.get() == '':
            messagebox.showerror('날짜 오류', '시작 날짜를 입력하세요.')
            return
        elif self.etr_end_date.get() == '':
            messagebox.showerror('날짜 오류', '마지막 날짜를 입력하세요.')
            return
        # 2. 엔트리에서 날짜 가져오기
        start_date = datetime.strptime(self.etr_start_date.get(), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.etr_end_date.get(), '%Y-%m-%d').date()
        # print(f'start_date : {start_date}, type : {type(start_date)}')
        # print(f'end_date : {end_date}, type : {type(end_date)}')

        # 3. 날짜 비교
        if start_date > end_date:
            messagebox.showerror('날짜 오류', '검색 시작 날짜가 검색 마지막 날짜 보다 큽니다.')
            return

        # 4. 데이터 필터링
        opt = self.get_option()
        filtered_dict = PandasMod.get_filtered_dr_dict(opt, start_date, end_date)

        # 5. treeview에 입력
        self.master.master.drTreeview.reset()
        self.master.master.drTreeview.set(filtered_dict)

    def get_option(self):
        return self.filter_option.get()

    def call_calendar(self, what_day):
        toplevel = Toplevel(self)
        toplevel.geometry("256x276+1500+100")
        dr_calendar = DailyReportCalendar.DailyReportCalendar(toplevel)
        dr_calendar.pack()
        self.what_day = what_day


if __name__ == '__main__':
    app = Tk()
    freight_info = DailyReportFilter(app)
    freight_info.config(text='운행일보 조회')
    freight_info.pack()

    app.mainloop()
