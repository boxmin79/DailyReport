from tkinter import *
import PandasMod
import ExcelMod
from tkinter import messagebox
from tkinter import filedialog


class DepositManagerButton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.btn_load_deposit = Button(self, width=20, text="입금내역 불러오기", command=self.load_deposit)
        self.btn_load_deposit.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_del_selected_dp_item = Button(self, width=20, text="선택항목 삭제(입금)",
                                               command=self.del_selected_dp_item)
        self.btn_del_selected_dp_item.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_match = Button(self, width=20, text="입금내역 매치시키기", command=self.matching_deposit)
        self.btn_match.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_manual_match = Button(self, width=20, text="입금내역 수동 매치",
                                       command=self.manual_matching_deposit)
        self.btn_manual_match.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_input_excel_match = Button(self, width=20, text="매치 리스트 엑셀입력",
                                            command=self.input_match_data)
        self.btn_input_excel_match.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_del_selected_nodp_item = Button(self, width=20, text="선택항목 삭제(미입금)",
                                                 command=self.del_selected_receivable_item)
        self.btn_del_selected_nodp_item.pack(side='left', expand=True, padx=3, pady=3)

        self.btn_match = Button(self, width=20, text="예외 항목 추가", takefocus=False,
                                command=self.add_exception)
        self.btn_match.pack(side='left', expand=True, padx=3, pady=3)
        
    def load_deposit(self):
        # 1. 입금 엑셀파일 읽기
        file_deposit = filedialog.askopenfilename(initialdir=r'D:/Users/realb', title='입급내역 불러오기',
                                                  filetypes=(("xls", "*.xls"), ("xlsx", "*.xlsx")))
        
        # 'xls'확인
        if file_deposit: 
            if file_deposit[list(file_deposit).index(''):] == ('.xlsx' or '.xlsm'):
                self.master.deposit_dict = PandasMod.get_deposit_dict(file_deposit, xls=False)
            else:  # file_deposit[list(file_deposit).index('.'):] == '.xls':
                # self.master.deposit_dict = PandasMod.get_deposit_dict(file_deposit)
                self.master.deposit_dict = PandasMod.get_deposit_dict(file_deposit)

        # 1-1 미입금 내역 파일 읽기
        self.master.receivable_dict = PandasMod.get_receivable_dict()

        # 2. 트리뷰 입력
        self.master.receivableTreeview.update_receivable_treeview(self.master.receivable_dict)
        self.master.depositTreeview.update_treeview_deposit(self.master.deposit_dict)

    def del_selected_dp_item(self):
        if self.master.depositTreeview.treeviewDeposit.focus() != '':
            iid = self.master.depositTreeview.treeviewDeposit.focus()
            self.master.depositTreeview.treeviewDeposit.delete(iid)
    
    def matching_deposit(self):
        # 입금 내역 리스트 가져오기
        dp_dict = self.master.deposit_dict.copy()

        # 미입금 리스트 가져오기
        re_dict = self.master.receivable_dict.copy()
        # print(receivable_dict)
        # 리스트 매치
        self.master.match_dict = self.get_match_list(dp_dict, re_dict)
        # print(self.master.match_dict)
        self.master.matchedTreeview.update_treeview_match(self.master.match_dict)

    def manual_matching_deposit(self):
        # 0. 입금내역 없으면
        if len(self.master.depositTreeview.treeviewDeposit.get_children()) == 0:
            messagebox.showerror('error', '입금내역을 불러오세요.')
        elif len(self.master.depositTreeview.treeviewDeposit.get_children()) >= 1:
            # 1. 입금내역 선택
            # print('입금내역을 선택하세요.')
            if len(self.master.depositTreeview.treeviewDeposit.selection()) == 0:
                messagebox.showerror('error', '입금내역을 선택하세요.')
            else:  # len(self.treeview_deposit.selection()) > 0:
                # 2. 미입금 내역 포커스
                if len(self.master.receivableTreeview.treeviewReceivable.selection()) == 0:
                    messagebox.showerror('error', '미입금내역을 선택하세요.')
                # 3. 입금 내역 매치
                else:  # if len(self.treeview_notdeposit.selection()) > 0:
                    # 입금내역 트리뷰 아이템 get
                    dp_items = self.master.depositTreeview.get_selected()
                    # 미입금내역 트리뷰 아이템 get
                    re_items = self.master.receivableTreeview.get_selected()
                    # items로 dict추출
                    dp_dict = {}
                    re_dict = {}
                    # print(self.master.deposit_dict)
                    # print(self.master.receivable_dict)
                    for dp_iid in dp_items:
                        dp_dict[dp_iid] = self.master.deposit_dict[dp_iid].copy()
                        # print(dp_items[dp_iid])
                        # print(self.master.deposit_dict[dp_iid])
                    for re_iid in re_items:
                        # print(re_items[re_iid])
                        # print(self.master.deposit_dict[re_iid])
                        re_dict[re_iid] = self.master.receivable_dict[re_iid].copy()

                    manual_match_dict = self.manual_matching_se(dp_dict, re_dict)
                    # print('manual_match_dict')
                    # for idx in manual_match_dict:
                    #     print(manual_match_dict[idx])
                    self.master.match_dict.update(manual_match_dict)
                    # print('== manual_match_dict 추가 self.master.match_dict ==')
                    # for idx in self.master.match_dict:
                    #     print(self.master.match_dict[idx])
                    self.master.matchedTreeview.add(manual_match_dict)

    def manual_matching_se(self, dp_dict, re_dict):
        manual_match_dict = {}
        # print('===== manual_matching_se =====')
        i = 1
        for re_idx in re_dict:
            # print(f're_dict[re_idx]:{re_idx}')
            # print(re_dict[re_idx])
            for dp_idx in dp_dict:
                # print(f'[dp_dict[dp_idx]:{dp_idx}')
                # print(dp_dict[dp_idx])
                if re_idx in manual_match_dict:
                    dup_idx = f'중복({re_idx}-{i})'
                    manual_match_dict[dup_idx] = merge_list_and_delete(dp_dict[dp_idx], re_dict[re_idx])
                    i += 1
                else:
                    manual_match_dict[re_idx] = merge_list_and_delete(dp_dict[dp_idx], re_dict[re_idx])

        self.del_treeview_list(list(dp_dict.keys()), list(re_dict.keys()))
        return manual_match_dict

    def input_match_data(self):
        if len(self.master.matchedTreeview.treeviewMatch.get_children()) == 0:
            messagebox.showerror('error', '매치 리스트가 없습니다.')
        elif len(self.master.matchedTreeview.treeviewMatch.get_children()) > 0:
            ExcelMod.input_match_data(self.master.match_dict)
            # match_dict = self.master.matchedTreeview.get_all()
            messagebox.showinfo('안내', '입금내역을 저장하였습니다.')

    def get_match_list(self, dp_dict, re_dict):
        # 1. 미입금 리스트 순환(for)
        for re_idx in re_dict:
            # print(nodp_item)
            # 2. 입금 리스트 순환(for)
            for dp_idx in dp_dict:
                # print(f'인덱스({i})', dp_item)
                # 3. 같은 금액 찾기
                vat_included = int((re_dict[re_idx]['합계금액'] * 11) / 10)  # 미입금 금액에 부가세 더한 금액
                # print(f'부가세포함 : {vat_included}', end='\t')
                # print(f"입금액 : {dp_dict[dp_idx]['입금액']}")
                if vat_included == dp_dict[dp_idx]['입금액']:  # 부가세 포함 금액과 입금액 비교
                    # print(f'부가세포함 : {vat_included}', end='\t')
                    # print(f"입금액 : {dp_dict[dp_idx]['입금액']}")
                    # 4. 이름 매치 시키기
                    # print(f"보낸분:{dp_dict[dp_idx]['보낸분']}, 화주명:{re_dict[re_idx]['화주명']}")
                    if match_same_name(dp_dict[dp_idx]['보낸분'], re_dict[re_idx]['화주명']):
                        # print(f"보낸분:{dp_dict[dp_idx]['보낸분']}, 화주명:{re_dict[re_idx]['화주명']}")
                        # print(dp_dict[dp_idx], '\n', re_dict[re_idx])
                        self.master.match_dict[re_idx] = merge_list_and_delete(dp_dict[dp_idx], re_dict[re_idx])
                        self.del_treeview_list([dp_idx], [re_idx])
                        del dp_dict[dp_idx]
                        break
        return self.master.match_dict

    def del_treeview_list(self, dp_num, re_num):
        for dp in dp_num:
            self.master.depositTreeview.treeviewDeposit.delete(str(dp))
        for re in re_num:
            self.master.receivableTreeview.treeviewReceivable.delete(str(re))

    def del_selected_receivable_item(self):
        if self.master.receivableTreeview.treeviewReceivable.focus() != '':
            iid = self.master.receivableTreeview.treeviewReceivable.focus()
            self.master.receivableTreeview.treeviewReceivable.delete(iid)
    
    def add_exception(self):
        if self.master.depositTreeview.treeviewDeposit.focus() != '':
            iid = self.master.depositTreeview.treeviewDeposit.focus()
            item = self.master.depositTreeview.treeviewDeposit.set(iid) 
            exception_name = item['보낸분']
        ExcelMod.add_exception(exception_name)
        

def match_same_name(sender, consignor):
    if sender == consignor:
        return True
    elif sender.replace('주식회사', '').strip() == consignor.replace('(주)', '').strip():
        return True
    elif sender in consignor:
        return True
    elif sender.replace('주식회사', '').strip() in consignor.replace('(주)', '').strip():
        return True
    elif consignor in sender:
        return True
    elif consignor.replace('(주)', '').strip() in sender.replace('주식회사', '').strip():
        return True
    elif sender[:4] in consignor:
        return True
    elif sender.replace('주식회사', '').strip()[:4] in consignor.replace('(주)', '').strip():
        return True
    elif consignor[:4] in sender:
        return True
    elif consignor.replace('(주)', '').strip()[:4] in sender.replace('주식회사', '').strip():
        return True
    else:
        return False


def merge_list_and_delete(dp_dict, re_dict):
    result = {'일보ID': re_dict['일보ID'], '배차시간': re_dict['배차시간'], '화주ID': re_dict['화주ID'],
              '화주명': re_dict['화주명'], '합계금액': re_dict['합계금액'], '입금일': dp_dict['입금일'],
              '보낸분': dp_dict['보낸분'], '입금액': dp_dict['입금액'], '빈칸': ''}
    return result


if __name__ == '__main__':
    app = Tk()
    app_widget = DepositManagerButton(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
