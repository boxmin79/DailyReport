from tkinter import *
import MakeCrop
import ImageToText
import ExcelMod
import PandasMod
from tkinter import messagebox


class DailyReportButton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # 운행일보 입력
        self.insert_button = Button(self, text='운행일보 입력', width=10, height=1,
                                    command=self.insert_dr_record)
        self.insert_button.pack(side='left', ipadx=5, ipady=5, padx=10, pady=5)

        # 운행일보 수정
        self.insert_button = Button(self, text='운행일보 수정', width=10, height=1,
                                    command=self.edit_dr_record)
        self.insert_button.pack(side='left', ipadx=5, ipady=5, padx=10, pady=5)

        # 선택이미지 변환
        self.button_img2text = Button(self, text='이미지변환', width=10, height=1,
                                      command=self.image_to_text)
        self.button_img2text.pack(side='left', ipadx=5, ipady=5, padx=10, pady=5)

        # 리셋
        self.button_reset = Button(self, text='리셋', width=10, height=1,
                                      command=self.reset_all_widget)
        self.button_reset.pack(side='left', ipadx=5, ipady=5, padx=10, pady=5)

        # 자동입력
        self.auto_insert_button = Button(self, text='자동 입력', width=10, height=1,
                                         command=self.auto_insert)
        self.auto_insert_button.pack(side='right', ipadx=5, ipady=5, padx=10, pady=5)

    def insert_dr_record(self, print_dicts=False):
        # 1. 화물번호 비교
        freight_number = self.master.master.freightInfo.etr_freight_number.get()
        business_number = self.master.master.consignorInfo.etr_business_number.get()
        if PandasMod.search_same_value(freight_number, '운행일보', '화물번호'):
            messagebox.showwarning('경고', '이미 입력된 운행일보 입니다.')
        else:
            if print_dicts:
                for key in self.master.master.freightInfo.get():
                    print(f'{key}: {self.master.master.freightInfo.get()[key]}')
                print()
                for key in self.master.master.consignorInfo.get():
                    print(f'{key}: {self.master.master.consignorInfo.get()[key]}')
                print()
                for key in self.master.master.paymentInfo.get():
                    print(f'{key}: {self.master.master.paymentInfo.get()[key]}')

            freight_info_dict = self.master.master.freightInfo.get()
            ExcelMod.input_dicts(freight_info_dict, '운행일보')
            payment_info_dict = self.master.master.paymentInfo.get()
            ExcelMod.input_dicts(payment_info_dict, '세금계산서')
            # 운송사 비교
            # freight_number = self.master.master.freightInfo.etr_freight_number.get()
            if not PandasMod.search_same_value(business_number, '운송사목록', '사업자번호'):
                consignor_info_dict = self.master.master.consignorInfo.get()
                ExcelMod.input_dicts(consignor_info_dict, '운송사목록')
            print('call "delete_focused_and_focus_next()"')
            # 이미지파일 리스트에 지우기(파일 이동)
            self.master.master.imageFile.delete_focused_and_focus_next()
            self.reset_all_widget()
            self.master.master.imageFile.set_count()
            messagebox.showinfo('입력', '운행일보를 입력하였습니다.')

    def reset_all_widget(self):
        self.master.master.freightInfo.reset()
        self.master.master.consignorInfo.reset()
        self.master.master.paymentInfo.reset()
        self.master.master.consignorTreeview.reset()
        self.master.master.csnTreeviewInfo.reset()
        self.master.master.update_csn_treeview()
        self.master.master.drTreeviewInfo.reset()
        self.master.master.update_dr_treeview()

    def image_to_text(self):
        print('Run "image_to_text(self)"')
        item = self.master.master.imageFile.get_item()
        path = self.master.master.imageFile.file_path
        print(f'path : {path}')
        print(f'item : {item}')
        print(f'list(item.values()) :  {list(item.values())}')
        # 1. 이미지 조각 가져오기
        crops = MakeCrop.make_crops(path, list(item.values())[1:])

        # 2. OCR인스턴트 생성
        freight_info_ocr = ImageToText.FreightInfoOCR(crops[0])
        print('Call "ImageToText.ConsignorInfoOCR(crops[1])"')
        consignor_info_ocr = ImageToText.ConsignorInfoOCR(crops[1])
        payment_info_ocr = ImageToText.PaymentInfoOCR(crops[2])

        # 3. 위젯에 텍스트 입력
        freight_info_dict = freight_info_ocr.get_dict()
        consignor_info_dict = consignor_info_ocr.get_dict()
        freight_info_dict.update({'화주명': consignor_info_dict['화주명']})
        payment_info_dict = payment_info_ocr.get_dict()

        self.master.master.freightInfo.set(freight_info_dict)
        self.master.master.consignorInfo.set(consignor_info_dict)
        self.master.master.paymentInfo.set(payment_info_dict)

        self.master.master.drTreeview.treeview_daily_report_selection_remove()
        self.master.master.drTreeviewInfo.reset()

    def edit_dr_record(self):
        messagebox.showinfo('수정', '운행일보를 수정하였습니다.')

    def auto_insert(self):
        pass


if __name__ == '__main__':
    app = Tk()
    freight_info = DailyReportButton(app)
    freight_info.config()
    freight_info.pack()

    app.mainloop()
