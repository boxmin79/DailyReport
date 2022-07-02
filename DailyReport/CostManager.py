from tkinter import *
import tkinter.font
import StatusBar
import CostManagerEntry
import CostManagerButton
import CostManagerTreeview
import PandasMod


class CostManager(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # 3-2 타이틀 레이블
        self.font_title = tkinter.font.Font(family='맑은 고딕', size=20)
        self.lbl_dpm_title = Label(self, text='비용 관리', font=self.font_title)
        self.lbl_dpm_title.pack(side='top', anchor='w')

        # 1. 상태바
        self.statusBar = StatusBar.StatusBar(self)
        self.statusBar.config(bg='gray')
        self.statusBar.pack(side='bottom', fill='x')

        # 2. 엔트리 프레임
        self.cmeFrame = Frame(self)
        self.cmeFrame.pack(side='left', anchor='n')

        # 2-1 엔트리 위젯
        self.costManagerEntry = CostManagerEntry.CostManagerEntry(self.cmeFrame)
        self.costManagerEntry.config()
        self.costManagerEntry.pack(side='top', expand=True, fill='both')

        # 2-2 엔트리 버튼
        self.costManagerButton = CostManagerButton.CostManagerButton(self.cmeFrame)
        self.costManagerButton.config()
        self.costManagerButton.pack(side='top', fill='x')

        # 3. 비용관리 트리뷰
        self.costManagerTreeview = CostManagerTreeview.CostManagerTreeview(self)
        self.costManagerTreeview.config()
        self.costManagerTreeview.pack(side='right', expand=True, fill='both')

        self.load_cost_list()

    def load_cost_list(self):
        cost_dict = PandasMod.get_cost_dict()
        # print(f"{cost_dict[0]['날짜']}, type:{type(cost_dict[0]['날짜'])}")
        # for idx in cost_dict:
        #     print(cost_dict[idx])
        self.costManagerTreeview.update_treeview_cost(cost_dict)


if __name__ == '__main__':
    app = Tk()
    app_widget = CostManager(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
