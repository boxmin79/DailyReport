from tkinter import *
from tkinter import messagebox
import ExcelMod


class CostManagerButton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self_button = Frame(self)
        self_button.pack(expand=True, fill='x')

        self.btn_input = Button(self_button, text='입력', width=10, command=self.input_cost_excel)
        self.btn_input.bind("<Return>", self.init_input_cost_excel)
        self.btn_input.pack(side=LEFT, anchor=E, padx=3, pady=3)  # , expand=True

        self.btn_edit = Button(self_button, text='수정', width=10, command=self.edit)
        self.btn_edit.pack(side=RIGHT, anchor=E, padx=3, pady=3)  # , expand=True

        self.btn_load = Button(self_button, text='로드', width=10)  # , command=self.insert_treeview)
        self.btn_load.pack(side=RIGHT, anchor=E, padx=3, pady=3)  # , expand=True

    def edit(self):
        pass

    def input_cost_excel(self):
        if self.master.master.costManagerEntry.etr_date.get() == '':
            messagebox.showerror('error', '날짜를 입력하세요')
            return
        elif self.master.master.costManagerEntry.cbo_sector.get() == '':
            messagebox.showerror('error', '분류를 입력하세요')
            return
        elif self.master.master.costManagerEntry.cbo_item.get() == '':
            messagebox.showerror('error', '항목을 입력하세요')
            return
        elif self.master.master.costManagerEntry.etr_item_cost.get() == '':
            messagebox.showerror('error', '금액을 입력하세요')
            return
        else:
            if self.master.master.costManagerEntry.cbo_item.get() == "디젤":
                if self.master.master.costManagerEntry.etr_unit_price.get() is None:
                    messagebox.showerror('error', '단가를 입력하세요')
                    return
                elif self.master.master.costManagerEntry.etr_quantity.get() is None:
                    messagebox.showerror('error', '수량을 입력하세요')
                    return
                elif self.master.master.costManagerEntry.etr_mileage.get() == '':
                    messagebox.showerror('error', '거리를 입력하세요')
                    return

        cost_dict = self.master.master.costManagerEntry.get()
        ExcelMod.input_cost_dict_to_excel(cost_dict)
        self.master.master.costManagerEntry.reset()
        self.master.master.costManagerTreeview.reset()
        self.master.master.load_cost_list()

    def init_input_cost_excel(self, event):
        self.input_cost_excel()

    # def insert_treeview(self):
    #     wb = load_workbook(r'D:/My Documents/운행일보/dr.xlsm')
    #     ws = wb['비용']
    #
    #     if ws.max_row > 2:
    #         i = 0
    #         for row in ws[2:ws.max_row]:
    #             if row[6].value is None:
    #                 mileage = ''
    #             else:
    #                 mileage = str(group(row[6].value)) + ' ㎞'
    #             if row[4].value is None:
    #                 unit_price = ''
    #             else:
    #                 unit_price = '￦ ' + str(row[4].value)
    #             if row[5].value is None:
    #                 quantity = ''
    #             else:
    #                 quantity = str(row[5].value)
    #             # print(row.value)
    #             if i % 2 == 0:
    #                 self.treeview_cost.insert(parent='', index='end', iid=str(i), text='',
    #                                           values=(row[0].value.date(), row[1].value, row[2].value,
    #                                                   '￦ ' + str(group(row[3].value)), unit_price, quantity, mileage),
    #                                           tags=('evenrow',))
    #             else:
    #                 self.treeview_cost.insert(parent='', index='end', iid=str(i), text='',
    #                                           values=(row[0].value.date(), row[1].value, row[2].value,
    #                                                   '￦ ' + str(group(row[3].value)), unit_price, quantity, mileage),
    #                                           tags=('oddrow',))
    #             self.treeview_cost.see(str(i))
    #             self.treeview_cost.selection_set(str(i))
    #             i += 1
    #
    #     else:
    #         self.treeview_cost.insert(parent='', index='end', iid=str(0), text='',
    #                                   values=(ws[2:ws.max_row][0].value.date(), ws[2:ws.max_row][1].value,
    #                                           ws[2:ws.max_row][2].value, '￦ ' + str(group(ws[2:ws.max_row][3].value)),
    #                                           str(group(ws[2:ws.max_row][4].value)) + ' ㎞'),
    #                                   tags=('evenrow',))
    #
    #     wb.close()


if __name__ == '__main__':
    app = Tk()
    app_widget = CostManagerButton(app)
    app_widget.config()
    app_widget.pack()

    app.mainloop()
