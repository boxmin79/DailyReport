from tkinter import *
import ExcelMod
from tkinter import messagebox


class ConsignorButton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # 입력
        self.button_regist = Button(self, text='등록', width=10,
                                    command=self.csn_regist)
        self.button_regist.pack(side='left', expand=True,
                                ipadx=5, ipady=5, padx=3, pady=3)
        # 수정
        self.button_edit = Button(self, text='수정', width=10,
                                  command=self.csn_edit)
        self.button_edit.pack(side='left', expand=True,
                              ipadx=5, ipady=5, padx=3, pady=3)
        # 초기화
        self.button_reset = Button(self, text='초기화', width=10,
                                   command=self.reset_csn_info)
        self.button_reset.pack(side='left', expand=True,
                               ipadx=5, ipady=5, padx=3, pady=3)
        # 삭제
        self.button_delete = Button(self, text='삭제', width=10,
                                    command=self.csn_delete)
        self.button_delete.pack(side='right', expand=True,
                                ipadx=5, ipady=5, padx=3, pady=3)

    def csn_regist(self):
        csn_dict = self.master.master.consignorInfo.get()
        ExcelMod.insert_csn_record_in_excel(csn_dict)
        messagebox.showinfo('등록', '새로운 운송사가 등록되었습니다.')
        self.master.master.update_csn_treeview()

    def csn_edit(self):
        print('====  <csn_edit>를 실행합니다. ====')
        # 1. 운송사ID 검색해서 row값 가져오기
        print('\tcsn_id를 설정합니다.')
        csn_id = self.master.master.consignorInfo.etr_consignorID.get()
        if csn_id == '':
            messagebox.showwarning('운송사 없음', '운송사를 선택하세요.')
        else:
            print(f'\t\tcsn_id : {csn_id}')
            print(f'\t입력할 row값을 가져옵니다.')
            row = ExcelMod.get_row_by_csn_id(int(csn_id))
            print(f'\t\trow = {row}')

            # 2. entry를 record에 저장
            print(f'\t운송사정보를 엔트리에서 가져옵니다.')
            csn_dict = csn_dict = self.master.master.consignorInfo.get()
            print(f'\t\t< csn_dict >\n')
            for idx in csn_dict:
                print(f'\t\t{idx}: {csn_dict[idx]}')
            # 3. row에 새로운 record입력
            print(f'\t엑셀에 새로운 내용을 입력합니다.')
            print('\t\t<ExcelMod.edit_csn_record(row, csn_dict)>호출')
            ExcelMod.edit_csn_record(row, csn_dict)
            # 4. 운송사 트리뷰 업데이트
            # self.update_treeview_same_consignor()
            messagebox.showinfo('수정', '운송사 내용을 수정하였습니다.')

    def reset_csn_info(self):
        self.master.master.consignorInfo.reset()
        self.master.master.update_csn_treeview()

    def csn_delete(self):
        choices = messagebox.askyesno('삭제', '운송사를 삭제하시겠습니까?')
        if choices:
            csn_id = self.master.master.consignorInfo.etr_consignorID.get()
            if csn_id == '':
                messagebox.showinfo('운송사 없음', '삭제할 운송사가 없습니다.')
                return
            else:
                row = ExcelMod.get_row_by_csn_id(int(csn_id))
                ExcelMod.delete_row(row)
                messagebox.showinfo('삭제', '운송사 내용을 삭제하였습니다.')
                self.master.master.update_csn_treeview()
                self.master.master.consignorInfo.reset()
                self.master.master.csnTreeviewInfo.reset()
        else:
            messagebox.showinfo('취소', '취소하였습니다.')


if __name__ == '__main__':
    app = Tk()
    freight_info = ConsignorButton(app)
    freight_info.config()
    freight_info.pack()

    app.mainloop()
