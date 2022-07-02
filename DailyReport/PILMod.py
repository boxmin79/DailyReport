from PIL import ImageTk, Image


def get_icon_img(file_name, w, h):
    cal_img = Image.open(file_name)
    resized_cal_img = cal_img.resize((w, h))
    result = ImageTk.PhotoImage(image=resized_cal_img)

    return result


def read_image(file_name):
    img = Image.open(file_name)
    return img


def resize_image(img):
    resize_img = img.resize((int(img.width * 0.65), int(img.height * 0.65)))
    return resize_img


def get_image_for_tk(img):
    tk_img = ImageTk.PhotoImage(image=img)
    return tk_img


def get_white065():
    white065 = 'white065.png'
    img_white065 = read_image(white065)
    tk_img_white065 = get_image_for_tk(img_white065)
    # print(img_white065.size)
    return tk_img_white065
