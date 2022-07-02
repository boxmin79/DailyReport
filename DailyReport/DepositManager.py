from tkinter import *
import tkinter.font
import StatusBar
import DepositManagerDepositTreeview
import DepositManagerMatchedTreeview
import DepositManagerReceivableTreeview
import DepositManagerButton


class DepositManager(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.match_dict = {}
        self.receivable_dict = {}
        self.deposit_dict = {}

        # 1. 상태바
        self.statusBar = StatusBar.StatusBar(self)
        self.statusBar.config(bg='gray')
        self.statusBar.pack(side='bottom', fill='x')

        # 3-2 타이틀 레이블
        self.font_title = tkinter.font.Font(family='맑은 고딕', size=20)
        self.lbl_dpm_title = Label(self, text='입금 관리', font=self.font_title)
        self.lbl_dpm_title.pack(side='top', anchor='w')

        # 2. 트리뷰프레임
        self.frmTreeview = Frame(self)
        self.frmTreeview.pack(side='top', expand=True, fill='both')

        # 2-1 미입금 리스트
        self.receivableTreeview = DepositManagerReceivableTreeview.ReceivableTreeview(self.frmTreeview)
        self.receivableTreeview.config()
        self.receivableTreeview.pack(side='left', anchor='n', expand=True, fill="both")

        # 2-2 매치 리스트
        self.matchedTreeview = DepositManagerMatchedTreeview.MatchedTreeview(self.frmTreeview)
        self.matchedTreeview.config()
        self.matchedTreeview.pack(side='left', anchor='n', expand=True, fill="both")

        # 2-3 입금 리스트
        self.depositTreeview = DepositManagerDepositTreeview.DepositTreeview(self.frmTreeview)
        self.depositTreeview.config()
        self.depositTreeview.pack(side='left', anchor='n', expand=True, fill="both")

        # 3. 버튼
        self.depositManagerButton = DepositManagerButton.DepositManagerButton(self)
        self.depositManagerButton.config()
        self.depositManagerButton.pack(side='top', fill='x')


if __name__ == '__main__':
    app = Tk()
    app_widget = DepositManager(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
