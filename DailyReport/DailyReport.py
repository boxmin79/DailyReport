from tkinter import Tk
from tkinter import Frame
import StatusBar
import DailyReportImageWindow
import DailyReportFreightInfo
import DailyReportPaymentInfo
import DailyReportButton
import DailyReportImageFileTreeview
import DailyReportConsignorInfo
import DailyReportConsignorButton
import DailyReportConsignorTreeview
import DailyReportConsignorTreeviewInfo
import DailyReportTreeview
import DailyReportTreeviewInfo
import DailyReportFilter
import PandasMod


class DailyReport(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.name = 'DailyReport'

        # 1. 상태바
        self.statusBar = StatusBar.StatusBar(self)
        self.statusBar.config(bg='gray')
        self.statusBar.pack(side='bottom', fill='x')

        # 2. 이미지 프레임
        self.imageWindow = DailyReportImageWindow.ImageWindow(self)
        self.imageWindow.config(bd=0)
        self.imageWindow.pack(side='left', fill='both', padx=3, pady=3)

        # 3. 화물정보, 결제정보, 이미지파일 트리뷰
        self.frm_2 = Frame(self)
        self.frm_2.pack(side='left', expand=True, fill='both')

        # 3-1 화물정보
        self.freightInfo = DailyReportFreightInfo.FreightInfo(self.frm_2)
        self.freightInfo.config(text='화물정보')
        self.freightInfo.pack(side='top', anchor='n', fill='x', padx=3, pady=3)

        # 3-2 결제정보
        self.paymentInfo = DailyReportPaymentInfo.PaymentInfo(self.frm_2)
        self.paymentInfo.config(text='결제정보')
        self.paymentInfo.pack(side='top', anchor='n', fill='x', padx=3, pady=3)

        # 3-3 운행일보 버튼
        self.drButton = DailyReportButton.DailyReportButton(self.frm_2)
        self.drButton.config()
        self.drButton.pack(side='top', anchor='n', fill='x', padx=3, pady=3)

        # 3-4 이미지 트리뷰
        self.imageFile = DailyReportImageFileTreeview.ImageFileTreeview(self.frm_2)
        self.imageFile.config(text='이미지파일')
        self.imageFile.pack(side='top', anchor='n', fill='x', padx=3, pady=3)

        # 4. 운송사정보, 운송사 트리뷰, 메세지 박스
        self.frm_3 = Frame(self)
        self.frm_3.pack(side='left', expand=True, fill='both')

        # 4-1 운송사정보
        self.consignorInfo = DailyReportConsignorInfo.ConsignorInfo(self.frm_3)
        self.consignorInfo.config(text='화주정보')
        self.consignorInfo.pack(side='top', anchor='n', fill='x', padx=3, pady=3)

        # 4-2 운송사버튼
        self.consignorButton = DailyReportConsignorButton.ConsignorButton(self.frm_3)
        self.consignorButton.config()  # relief='solid', bd=1)
        self.consignorButton.pack(side='top', anchor='n', fill='x')

        # 4-3 운송사 트리뷰
        self.consignorTreeview = DailyReportConsignorTreeview.ConsignorTreeview(self.frm_3)
        self.consignorTreeview.config(text='운송사 리스트')
        self.consignorTreeview.pack(side='top', padx=3, pady=3, fill='x')

        # 4-4 운송사 트리뷰 정보 박스
        self.csnTreeviewInfo = DailyReportConsignorTreeviewInfo.ConsignorTreeviewInfo(self.frm_3)
        self.csnTreeviewInfo.config(text='트리뷰 정보')
        self.csnTreeviewInfo.pack(side='top', anchor='n', expand=True, fill='both',
                                  ipadx=3, ipady=3, padx=3, pady=3)

        # 5. 운행일보 트리뷰
        self.frm_4 = Frame(self)
        self.frm_4.pack(side='left', expand=True, fill='both')

        # 5-1 운행일보 트리뷰 필터
        self.drTreeviewFilter = DailyReportFilter.DailyReportFilter(self.frm_4)
        self.drTreeviewFilter.config(text='운행일보 조회')
        self.drTreeviewFilter.pack(side='top', fill='x', padx=3, pady=3)

        # 5-2 운행일보 트리뷰
        self.drTreeview = DailyReportTreeview.DailyReportTreeview(self.frm_4)
        self.drTreeview.config(text='운행일보 리스트')
        self.drTreeview.pack(side='top', expand=True, fill='both', padx=3, pady=3)

        # 5-3 운행일보 트리뷰 정보창
        self.drTreeviewInfo = DailyReportTreeviewInfo.DailyReportTreeviewInfo(self.frm_4)
        self.drTreeviewInfo.config(text='트리뷰 정보')
        self.drTreeviewInfo.pack(side='top', anchor='n', expand=True, fill='both',
                                  ipadx=3, ipady=3, padx=3, pady=3)

        self.update_csn_treeview()
        self.update_dr_treeview()

    def confirm(self):
        print(self.name)

    def update_csn_treeview(self):
        print('Run <DailyReport.update_csn_treeview()')
        csn_dict = PandasMod.get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '운송사목록', return_by_dict=True)
        self.consignorTreeview.update_csn_treeview(csn_dict)

        print('Done <DailyReport.update_csn_treeview()')

    def update_dr_treeview(self):
        print('Run <DailyReport.update_dr_treeview()')
        self.drTreeview.update_treeview_daily_report()
        print('Done <DailyReport.update_dr_treeview()')


if __name__ == '__main__':
    app = Tk()
    app_widget = DailyReport(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
