from tkinter import *
from datetime import datetime, date
from tkinter import font
from dateutil.relativedelta import relativedelta
import calendar
import PILMod


class DailyReportCalendar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.font = font.Font(size=11, weight='bold')

        self.right_arrow_img = PILMod.get_icon_img('C:/Users/realb/PycharmProjects/DailyReport/Icon/right_arrow.png',
                                                   20, 20)
        self.left_arrow_img = PILMod.get_icon_img('C:/Users/realb/PycharmProjects/DailyReport/Icon/left_arrow.png',
                                                  20, 20)
        self.dt = get_now()
        self.dt_str = datetime_to_str(self.dt)
        self.day_of_week = ['일', '월', '화', '수', '목', '금', '토', '일']
        self.cal_dict = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '',
                         10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '', 17: '', 18: '', 19: '',
                         20: '', 21: '', 22: '', 23: '', 24: '', 25: '', 26: '', 27: '', 28: '', 29: '',
                         30: '', 31: '', 32: '', 33: '', 34: '', 35: '', 36: '', 37: '', 38: '', 39: '',
                         40: '', 41: ''}

        self.etr_vals = []

        self.sel_date = datetime.today()
        # # 1. 타이틀
        # self.font_title = tkinter.font.Font(family='맑은 고딕', size=14)
        # self.lblCalendarTitle = Label(self, text='달력', font=self.font_title)
        # self.lblCalendarTitle.pack(side='top', anchor='w')
        # 2 월이동버튼
        self.frmSelectMonth = Frame(self)
        self.frmSelectMonth.pack(side='top', fill='x')
        # 2-1 이전 버튼
        self.btnBefore = Button(self.frmSelectMonth, bg='lemon chiffon', fg='yellow',
                                image=self.left_arrow_img, command=self.get_before_month)
        self.btnBefore.pack(side='left', ipadx=2, ipady=2, padx=2)
        # 2-2 다음 버튼
        self.btnNext = Button(self.frmSelectMonth, bg='lemon chiffon', fg='yellow',
                              image=self.right_arrow_img, command=self.get_next_month)
        self.btnNext.pack(side='right', ipadx=2, ipady=2, padx=2)
        # 2-3 월표시 레이블
        self.textYearMonth = StringVar()
        self.textYearMonth.set(self.dt_str)
        self.lblYearMonth = Label(self.frmSelectMonth, font=self.font, bg='dodgerblue', textvariable=self.textYearMonth)
        self.lblYearMonth.pack(side='left', ipady=1, fill='x', expand=True, anchor='center')

        # 3 달력
        self.frmCalendar = Frame(self)
        self.frmCalendar.pack(side='top')
        # 3-1 요일

        self.lblCalSun = Label(self.frmCalendar, font=self.font, text=self.day_of_week[0], relief='solid', bd=1,
                               bg='red', fg='yellow')
        self.lblCalSun.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=1)

        self.lblCalMon = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[1], relief='solid', bd=1)
        self.lblCalMon.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=2)

        self.lblCalTue = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[2], relief='solid', bd=1)
        self.lblCalTue.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=3)

        self.lblCalWed = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[3], relief='solid', bd=1)
        self.lblCalWed.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=4)

        self.lblCalThu = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[4], relief='solid', bd=1)
        self.lblCalThu.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=5)

        self.lblCalFri = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[5], relief='solid', bd=1)
        self.lblCalFri.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=6)

        self.lblCalSat = Label(self.frmCalendar, font=self.font,  text=self.day_of_week[6], relief='solid', bd=1)
        self.lblCalSat.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=1, row=1, column=7)

        # 1주 차
        self.textCal1_1 = StringVar()
        self.btnCal1_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                                # bg='red', fg='cyan', disabledforeground='black',
                                justify='right', command=lambda: self.get_date(0),
                                textvariable=self.textCal1_1) 
        self.btnCal1_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_1.get()))
        self.btnCal1_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=1)

        self.textCal1_2 = StringVar()
        self.btnCal1_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,                                
                                justify='right', command=lambda: self.get_date(1),
                                textvariable=self.textCal1_2) 
        self.btnCal1_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_2.get()))
        self.btnCal1_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=2)

        self.textCal1_3 = StringVar()
        self.btnCal1_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                                
                                justify='right', command=lambda: self.get_date(2),
                                textvariable=self.textCal1_3) 
        self.btnCal1_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_3.get()))
        self.btnCal1_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=3)

        self.textCal1_4 = StringVar()
        self.btnCal1_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                                
                                justify='right', command=lambda: self.get_date(3),
                                textvariable=self.textCal1_4) 
        self.btnCal1_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_4.get()))
        self.btnCal1_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=4)

        self.textCal1_5 = StringVar()
        self.btnCal1_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(4),
                                textvariable=self.textCal1_5) 
        self.btnCal1_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_5.get()))
        self.btnCal1_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=5)

        self.textCal1_6 = StringVar()
        self.btnCal1_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(5),
                                textvariable=self.textCal1_6) 
        self.btnCal1_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_6.get()))
        self.btnCal1_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=6)

        self.textCal1_7 = StringVar()
        self.btnCal1_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(6),
                                textvariable=self.textCal1_7) 
        self.btnCal1_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal1_7.get()))
        self.btnCal1_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=2, column=7)

        # 2주 차
        self.textCal2_1 = StringVar()
        self.btnCal2_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                                justify='right', command=lambda: self.get_date(7),
                                textvariable=self.textCal2_1) 
        self.btnCal2_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_1.get()))
        self.btnCal2_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=1)

        self.textCal2_2 = StringVar()
        self.btnCal2_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(8),
                                textvariable=self.textCal2_2) 
        self.btnCal2_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_2.get()))
        self.btnCal2_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=2)

        self.textCal2_3 = StringVar()
        self.btnCal2_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(9),
                                textvariable=self.textCal2_3) 
        self.btnCal2_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_3.get()))
        self.btnCal2_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=3)

        self.textCal2_4 = StringVar()
        self.btnCal2_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(10),
                                textvariable=self.textCal2_4) 
        self.btnCal2_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_4.get()))
        self.btnCal2_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=4)

        self.textCal2_5 = StringVar()
        self.btnCal2_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(11),
                                textvariable=self.textCal2_5) 
        self.btnCal2_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_5.get()))
        self.btnCal2_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=5)

        self.textCal2_6 = StringVar()
        self.btnCal2_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(12),
                                textvariable=self.textCal2_6) 
        self.btnCal2_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_6.get()))
        self.btnCal2_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=6)

        self.textCal2_7 = StringVar()
        self.btnCal2_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(13),
                                textvariable=self.textCal2_7) 
        self.btnCal2_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal2_7.get()))
        self.btnCal2_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=3, column=7)

        # 3주 차
        self.textCal3_1 = StringVar()
        self.btnCal3_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                              
                                justify='right', command=lambda: self.get_date(14),
                                textvariable=self.textCal3_1) 
        self.btnCal3_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_1.get()))
        self.btnCal3_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=1)

        self.textCal3_2 = StringVar()
        self.btnCal3_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(15),
                                textvariable=self.textCal3_2) 
        self.btnCal3_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_2.get()))
        self.btnCal3_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=2)

        self.textCal3_3 = StringVar()
        self.btnCal3_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(16),
                                textvariable=self.textCal3_3) 
        self.btnCal3_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_3.get()))
        self.btnCal3_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=3)

        self.textCal3_4 = StringVar()
        self.btnCal3_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(17),
                                textvariable=self.textCal3_4) 
        self.btnCal3_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_4.get()))
        self.btnCal3_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=4)

        self.textCal3_5 = StringVar()
        self.btnCal3_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(18),
                                textvariable=self.textCal3_5) 
        self.btnCal3_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_5.get()))
        self.btnCal3_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=5)

        self.textCal3_6 = StringVar()
        self.btnCal3_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(19),
                                textvariable=self.textCal3_6) 
        self.btnCal3_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_6.get()))
        self.btnCal3_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=6)

        self.textCal3_7 = StringVar()
        self.btnCal3_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(20),
                                textvariable=self.textCal3_7) 
        self.btnCal3_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal3_7.get()))
        self.btnCal3_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=4, column=7)

        # 4주 차
        self.textCal4_1 = StringVar()
        self.btnCal4_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                              
                                justify='right', command=lambda: self.get_date(21),
                                textvariable=self.textCal4_1) 
        self.btnCal4_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_1.get()))
        self.btnCal4_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=1)

        self.textCal4_2 = StringVar()
        self.btnCal4_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(22),
                                textvariable=self.textCal4_2) 
        self.btnCal4_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_2.get()))
        self.btnCal4_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=2)

        self.textCal4_3 = StringVar()
        self.btnCal4_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(23),
                                textvariable=self.textCal4_3) 
        self.btnCal4_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_3.get()))
        self.btnCal4_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=3)

        self.textCal4_4 = StringVar()
        self.btnCal4_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(24),
                                textvariable=self.textCal4_4) 
        self.btnCal4_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_4.get()))
        self.btnCal4_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=4)

        self.textCal4_5 = StringVar()
        self.btnCal4_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(25),
                                textvariable=self.textCal4_5) 
        self.btnCal4_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_5.get()))
        self.btnCal4_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=5)

        self.textCal4_6 = StringVar()
        self.btnCal4_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(26),
                                textvariable=self.textCal4_6) 
        self.btnCal4_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_6.get()))
        self.btnCal4_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=6)

        self.textCal4_7 = StringVar()
        self.btnCal4_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(27),
                                textvariable=self.textCal4_7) 
        self.btnCal4_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal4_7.get()))
        self.btnCal4_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=5, column=7)

        # 5주 차
        self.textCal5_1 = StringVar()
        self.btnCal5_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                              
                                justify='right', command=lambda: self.get_date(28),
                                textvariable=self.textCal5_1) 
        self.btnCal5_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_1.get()))
        self.btnCal5_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=1)

        self.textCal5_2 = StringVar()
        self.btnCal5_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(29),
                                textvariable=self.textCal5_2) 
        self.btnCal5_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_2.get()))
        self.btnCal5_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=2)

        self.textCal5_3 = StringVar()
        self.btnCal5_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(30),
                                textvariable=self.textCal5_3) 
        self.btnCal5_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_3.get()))
        self.btnCal5_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=3)

        self.textCal5_4 = StringVar()
        self.btnCal5_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(31),
                                textvariable=self.textCal5_4) 
        self.btnCal5_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_4.get()))
        self.btnCal5_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=4)

        self.textCal5_5 = StringVar()
        self.btnCal5_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(32),
                                textvariable=self.textCal5_5) 
        self.btnCal5_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_5.get()))
        self.btnCal5_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=5)

        self.textCal5_6 = StringVar()
        self.btnCal5_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(33),
                                textvariable=self.textCal5_6) 
        self.btnCal5_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_6.get()))
        self.btnCal5_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=6)

        self.textCal5_7 = StringVar()
        self.btnCal5_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(34),
                                textvariable=self.textCal5_7) 
        self.btnCal5_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal5_7.get()))
        self.btnCal5_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=6, column=7)

        # 6주 차
        self.textCal6_1 = StringVar()
        self.btnCal6_1 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font,
                              
                                justify='right', command=lambda: self.get_date(35),
                                textvariable=self.textCal6_1) 
        self.btnCal6_1.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_1.get()))
        self.btnCal6_1.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=1)

        self.textCal6_2 = StringVar()
        self.btnCal6_2 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(36),
                                textvariable=self.textCal6_2) 
        self.btnCal6_2.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_2.get()))
        self.btnCal6_2.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=2)

        self.textCal6_3 = StringVar()
        self.btnCal6_3 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(37),
                                textvariable=self.textCal6_3) 
        self.btnCal6_3.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_3.get()))
        self.btnCal6_3.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=3)

        self.textCal6_4 = StringVar()
        self.btnCal6_4 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(38),
                                textvariable=self.textCal6_4) 
        self.btnCal6_4.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_4.get()))
        self.btnCal6_4.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=4)

        self.textCal6_5 = StringVar()
        self.btnCal6_5 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(39),
                                textvariable=self.textCal6_5) 
        self.btnCal6_5.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_5.get()))
        self.btnCal6_5.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=5)

        self.textCal6_6 = StringVar()
        self.btnCal6_6 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(40),
                                textvariable=self.textCal6_6) 
        self.btnCal6_6.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_6.get()))
        self.btnCal6_6.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=6)

        self.textCal6_7 = StringVar()
        self.btnCal6_7 = Button(self.frmCalendar, state='disabled', relief='flat', font=self.font, 
                                justify='right', command=lambda: self.get_date(41),
                                textvariable=self.textCal6_7) 
        self.btnCal6_7.config()  # .bind('<ButtonRelease-1>', self.print_date)  # (self.btnCal6_7.get()))
        self.btnCal6_7.grid(sticky='sewn', padx=2, pady=2, ipadx=1, ipady=0, row=7, column=7)

        self.set()
        print(f'==================\n'
              f'{self.sel_date}\n'
              f'==================')
        # self.etr_vals = self.get_entry_value_list()

    def get_before_month(self):
        self.dt = self.dt - relativedelta(months=1)
        self.textYearMonth.set(datetime_to_str(self.dt))
        self.reset()
        self.set()
        # self.etr_vals = self.get_entry_value_list()

    def get_next_month(self):
        self.dt = self.dt + relativedelta(months=1)
        self.textYearMonth.set(datetime_to_str(self.dt))
        self.reset()
        self.set()
        # self.etr_vals = self.get_entry_value_list()

    def get_start_day_of_week(self):
        # print(f'{self.dt} {self.day_of_week[self.dt.weekday()]}')
        # print(f'시작요일 = {self.day_of_week[month_range[0]]}')
        return calendar.monthrange(self.dt.year, self.dt.month)

    def get_text_var_list(self):
        return [self.textCal1_1, self.textCal1_2, self.textCal1_3, self.textCal1_4, self.textCal1_5, self.textCal1_6,
                self.textCal1_7,
                self.textCal2_1, self.textCal2_2, self.textCal2_3, self.textCal2_4, self.textCal2_5, self.textCal2_6,
                self.textCal2_7,
                self.textCal3_1, self.textCal3_2, self.textCal3_3, self.textCal3_4, self.textCal3_5, self.textCal3_6,
                self.textCal3_7,
                self.textCal4_1, self.textCal4_2, self.textCal4_3, self.textCal4_4, self.textCal4_5, self.textCal4_6,
                self.textCal4_7,
                self.textCal5_1, self.textCal5_2, self.textCal5_3, self.textCal5_4, self.textCal5_5, self.textCal5_6,
                self.textCal5_7,
                self.textCal6_1, self.textCal6_2, self.textCal6_3, self.textCal6_4, self.textCal6_5, self.textCal6_6,
                self.textCal6_7]

    def get_entry_list(self):
        return [self.btnCal1_1, self.btnCal1_2, self.btnCal1_3, self.btnCal1_4, self.btnCal1_5, self.btnCal1_6,
                self.btnCal1_7,
                self.btnCal2_1, self.btnCal2_2, self.btnCal2_3, self.btnCal2_4, self.btnCal2_5, self.btnCal2_6,
                self.btnCal2_7,
                self.btnCal3_1, self.btnCal3_2, self.btnCal3_3, self.btnCal3_4, self.btnCal3_5, self.btnCal3_6,
                self.btnCal3_7,
                self.btnCal4_1, self.btnCal4_2, self.btnCal4_3, self.btnCal4_4, self.btnCal4_5, self.btnCal4_6,
                self.btnCal4_7,
                self.btnCal5_1, self.btnCal5_2, self.btnCal5_3, self.btnCal5_4, self.btnCal5_5, self.btnCal5_6,
                self.btnCal5_7,
                self.btnCal6_1, self.btnCal6_2, self.btnCal6_3, self.btnCal6_4, self.btnCal6_5, self.btnCal6_6,
                self.btnCal6_7]

    def reset(self):
        text_vars = self.get_text_var_list()
        entrys = self.get_entry_list()

        for i in range(0, len(text_vars)):
            text_vars[i].set('')
            entrys[i].config(state='disabled', relief='flat', bg='white smoke', fg='black')
            self.cal_dict[i] = ''

    def set(self):
        text_var_list = self.get_text_var_list()
        entry_list = self.get_entry_list()
        rg = self.get_start_day_of_week()
        print(rg)
        for i in list(range(1, rg[1]+1)):
            text_var_list[i+rg[0]].set(str(i))
            if (i+rg[0]) % 7 == 0:
                entry_list[i+rg[0]].config(state='normal', relief='raised', bg='red', fg='yellow')
            else:
                entry_list[i + rg[0]].config(state='normal', relief='raised')
            self.cal_dict[i+rg[0]] = i
            # if (rg[0]) == 0:
            #     entry_list[i + rg[0]].config(bg='red')

    def get_date(self, day_idx):
        year = self.dt.year
        month = self.dt.month
        day = self.cal_dict[day_idx]
        sel_date = date(year, month, day)
        if self.master.master.what_day == 'start':
            print('start')
            self.master.master.text_start_date.set(sel_date)
        if self.master.master.what_day == 'end':
            print('end')
            self.master.master.text_end_date.set(sel_date)
        self.master.destroy()


def get_now():
    return datetime.now()


def datetime_to_str(dt):
    # print(dt.strftime("%Y년 %m월"))
    return dt.strftime("%Y년 %m월")


if __name__ == '__main__':
    app = Tk()
    app_widget = DailyReportCalendar(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()

    # def get_entry_value_list(self):
    #     return [self.btnCal1_1.get(), self.btnCal1_2.get(), self.btnCal1_3.get(), self.btnCal1_4.get(),
    #             self.btnCal1_5.get(), self.btnCal1_6.get(), self.btnCal1_7.get(),
    #             self.btnCal2_1.get(), self.btnCal2_2.get(), self.btnCal2_3.get(), self.btnCal2_4.get(),
    #             self.btnCal2_5.get(), self.btnCal2_6.get(), self.btnCal2_7.get(),
    #             self.btnCal3_1.get(), self.btnCal3_2.get(), self.btnCal3_3.get(), self.btnCal3_4.get(),
    #             self.btnCal3_5.get(), self.btnCal3_6.get(), self.btnCal3_7.get(),
    #             self.btnCal4_1.get(), self.btnCal4_2.get(), self.btnCal4_3.get(), self.btnCal4_4.get(),
    #             self.btnCal4_5.get(), self.btnCal4_6.get(), self.btnCal4_7.get(),
    #             self.btnCal5_1.get(), self.btnCal5_2.get(), self.btnCal5_3.get(), self.btnCal5_4.get(),
    #             self.btnCal5_5.get(), self.btnCal5_6.get(), self.btnCal5_7.get(),
    #             self.btnCal6_1.get(), self.btnCal6_2.get(), self.btnCal6_3.get(), self.btnCal6_4.get(),
    #             self.btnCal6_5.get(), self.btnCal6_6.get(), self.btnCal6_7.get()]
