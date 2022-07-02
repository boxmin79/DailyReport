from tkinter import LabelFrame
from tkinter import IntVar
from tkinter import Radiobutton
from tkinter import Label
from tkinter import Frame
import PILMod


class ImageWindow(LabelFrame):
    def __init__(self, master):
        LabelFrame.__init__(self, master)

        # 옵션버튼 프레임
        self.frame_radiobutton_img_show = LabelFrame(self, text='이미지선택')
        self.frame_radiobutton_img_show.pack(side='top', fill='x')  # , padx=3, pady=3)

        # 옵션버튼
        self.radiobutton_img_show_var = IntVar()
        self.radiobutton_freight_img = Radiobutton(self.frame_radiobutton_img_show, text='화물정보', value=0,
                                                   variable=self.radiobutton_img_show_var,
                                                   command=self.show_image_by_radio_button)

        self.radiobutton_freight_img.pack(side='left')
        self.radiobutton_consignor_img = Radiobutton(self.frame_radiobutton_img_show, text='화주정보', value=1,
                                                     variable=self.radiobutton_img_show_var,
                                                     command=self.show_image_by_radio_button)

        self.radiobutton_consignor_img.pack(side='left')
        self.radiobutton_payment_img = Radiobutton(self.frame_radiobutton_img_show, text='결제정보', value=2,
                                                   variable=self.radiobutton_img_show_var,
                                                   command=self.show_image_by_radio_button)
        self.radiobutton_payment_img.pack(side='left')

        # 이미지 프레임
        self.image_frame = Frame(self, relief='solid', bd=1)
        self.image_frame.pack(side='top', fill='both')  # , padx=3, pady=3)

        self.lbl_image = Label(self.image_frame)
        self.lbl_image.pack(ipadx=3, ipady=3)

        self.white065 = PILMod.get_white065()
        self.show_image(self.white065)

    def show_image(self, img):
        self.lbl_image.config(image=img)
        self.lbl_image.image = img

    def show_image_by_radio_button(self):
        item = self.master.imageFile.get_item()
        if item:
            path = self.master.imageFile.file_path
            tkimg = self.get_image(path, item)
            self.show_image(tkimg)

    def get_option(self):
        return self.radiobutton_img_show_var.get()

    def get_image(self, path, item):
        opt = self.get_option()
        opt_key = '화물정보'
        if opt == 1:
            opt_key = '화주정보'
        elif opt == 2:
            opt_key = '결제정보'
        img_file_name = path + item[opt_key]
        img = PILMod.read_image(img_file_name)
        resized_img = PILMod.resize_image(img)
        tkimg = PILMod.get_image_for_tk(resized_img)
        return tkimg





