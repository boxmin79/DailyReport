from tkinter import *
import tkinter.ttk as ttk
import os
import shutil


class ImageFileTreeview(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        self.file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/'

        # 파일버튼
        self.frm_button = Frame(self)
        self.frm_button.pack(fill='x')

        self.file_frame = Frame(self.frm_button)
        self.file_frame.pack(side='left', anchor='n', expand=True, fill="x", ipadx=3, padx=5, pady=5)

        self.btn_add_file = Button(self.file_frame, padx=5, pady=3, width=10, text="파일로드", command=self.add_file)
        self.btn_add_file.pack(side='left', anchor='sw')

        # 리스트박스 카운터
        self.list_counter_frame = Frame(self.frm_button)
        self.list_counter_frame.pack(side='right', anchor='se', expand=False)

        self.count_label = Label(self.list_counter_frame, width=4)
        self.count_label.pack(side='right', anchor='e')
        self.count_label.config(text=str(0))

        # 트리뷰
        self.frm_treeview = Frame(self)
        self.frm_treeview.pack(fill='x')

        self.scrollbar = Scrollbar(self.frm_treeview)
        self.scrollbar.pack(side="right", fill="y")

        self.treeview_file = ttk.Treeview(self.frm_treeview, selectmode="browse", height=6,
                                          yscrollcommand=self.scrollbar.set)
        self.treeview_file.bind('<ButtonRelease-1>', self.show_dr_img)
        self.treeview_file.pack(side='left', expand=True, fill="both", padx=3, pady=3)
        self.scrollbar.config(command=self.treeview_file.yview)

        # 트리뷰 설정
        self.treeview_file["columns"] = ("번호", "화물정보", "화주정보", "결제정보")

        self.treeview_file.column('#0', width=0, stretch=NO)
        self.treeview_file.column('번호', anchor=CENTER, width=10)
        self.treeview_file.column('화물정보', anchor=W, width=100)
        self.treeview_file.column('화주정보', anchor=W, width=100)
        self.treeview_file.column('결제정보', anchor=W, width=100)

        self.treeview_file.heading('#0')
        self.treeview_file.heading('번호', text='번호', anchor=CENTER)
        self.treeview_file.heading('화물정보', text='화물정보', anchor=W)
        self.treeview_file.heading('화주정보', text='화주정보', anchor=W)
        self.treeview_file.heading('결제정보', text='결제정보', anchor=W)

        self.treeview_file.tag_configure('oddrow', background='white')
        self.treeview_file.tag_configure('evenrow', background='lightgray')\


    def delete_focus(self):
        iid = self.treeview_file.focus()
        self.treeview_file.delete(iid)

    def get_next_iid(self, focused_iid):
        return self.treeview_file.next(focused_iid)

    def set_focus(self, iid):
        self.treeview_file.focus(iid)

    def set_next_focus(self, iid):
        next_iid = self.get_next_iid(iid)
        self.set_focus(next_iid)

    def delete_focused_and_focus_next(self):
        print('Run "delete_focused_and_focus_next()"')
        iid = self.treeview_file.focus()  # 포커스 iid
        next_iid = self.treeview_file.next(iid)  # 다음 iid
        print(f'next_iid : {next_iid}')
        print('Call "move_image_file()"')
        self.move_image_file(iid)  # iid 실제 파일 이동
        self.treeview_file.delete(iid)  # iid 트리뷰에서 제거

        if next_iid != '':
            self.treeview_file.focus(next_iid)  # 다음 iid 포커스(선택)
            item = self.get_item()
            tkimg = self.master.master.imageWindow.get_image(self.file_path, item)
            self.master.master.imageWindow.show_image(tkimg)

    def move_image_file(self, iid):
        print('Run "move_image_file()"')
        file_sets = self.treeview_file.set(iid)
        print(f'file_sets : {file_sets}')
        src = 'C:/Users/realb/PycharmProjects/DailyReport/img/dr/'
        dst = 'D:/dr_img_backup/'
        # dst = 'C:/Users/realb/PycharmProjects/DailyReport/img/dr/old/'
        shutil.move(src + file_sets['화물정보'], dst + file_sets['화물정보'])
        shutil.move(src + file_sets['화주정보'], dst + file_sets['화주정보'])
        shutil.move(src + file_sets['결제정보'], dst + file_sets['결제정보'])
        print('Done "move_image_file()"')

    def get_item(self):
        if self.treeview_file.focus():
            iid = self.treeview_file.focus()
            return self.treeview_file.set(iid)
        else:
            return {}

    def show_dr_img(self, event):
        item = self.get_item()
        tkimg = self.master.master.imageWindow.get_image(self.file_path, item)
        self.master.master.imageWindow.show_image(tkimg)

    def add_file(self):
        file_list = os.listdir(self.file_path)
        if 'old' in file_list:
            file_list.remove('old')
        # print(file_list)
        self.set(file_list)

    def reset(self):
        self.treeview_file.delete(*self.treeview_file.get_children())

    def update_file_treeview(self, file_list):
        self.reset()
        self.set(file_list)

    def set(self, file_list):
        idx = 1
        for record in [file_list[i:i + 3] for i in range(0, len(file_list), 3)]:
            if idx % 2 == 0:
                self.treeview_file.insert(parent='', index='end', iid=str(idx), text='',
                                          values=(idx, record[0], record[1], record[2]), tags=('evenrow',))
            else:
                self.treeview_file.insert(parent='', index='end', iid=str(idx), text='',
                                          values=(idx, record[0], record[1], record[2]), tags=('oddrow',))

            idx += 1
        self.set_count()

    def set_count(self):
        count = len(self.treeview_file.get_children())
        self.count_label.config(text=str(count))


if __name__ == '__main__':
    app = Tk()
    freight_info = ImageFileTreeview(app)
    freight_info.config(text='이미지파일')
    freight_info.pack()

    app.mainloop()
