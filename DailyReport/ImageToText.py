import cv2
import MakeCrop
import numpy as np
import cv2mod
import datetime
# from datetime import date
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'c:/Program Files/Tesseract-OCR/tesseract'


class FreightInfoOCR:
    def __init__(self, freight_crops):
        self.crops_lenth = len(freight_crops)
        self.freight_crops = freight_crops
        # print(self.crops_lenth)
        self.load_date = None
        self.unload_date = None
        self.load_method = None
        self.unload_method = None
        self.distance = None
        self.consoldation = None
        self.quantity = None
        self.unit = None
        self.freight_info_dict = self.set_freight_info_dict()

    def get_dict(self):
        return self.freight_info_dict

    def print_dict(self):
        for keys in self.freight_info_dict:
            print(f'{keys}: {self.freight_info_dict[keys]}')
        print()

    def set_freight_info_dict(self):
        freight_info_dict = {}
        freight_info_dict.update(self.get_load_date())
        freight_info_dict.update(self.get_cargo_number())
        freight_info_dict.update(self.get_load_location_info())
        freight_info_dict.update(self.get_unload_location_info())
        freight_info_dict.update(self.get_distance())
        freight_info_dict.update(self.get_load_unload_date())
        freight_info_dict.update(self.get_load_unload_method())
        freight_info_dict.update(self.get_freight_info())
        freight_info_dict.update(self.get_quantity())
        freight_info_dict.update(self.get_unit())
        freight_info_dict.update(self.get_consoldation())
        freight_info_dict.update(self.get_truck_class())
        freight_info_dict.update(self.get_truck_type())
        if self.crops_lenth > 15:
            freight_info_dict.update(self.get_load_weight())
            freight_info_dict.update(self.get_how_to_trans())
        else:
            freight_info_dict.update({'적재중량': '5.5톤', '운행방법': '편도'})
        return freight_info_dict

    def show_crops(self):
        i = 0
        for crop in self.freight_crops:
            cv2.imshow(f'self.freight_crops{i}', crop)
            i += 1

    def get_load_date(self):
        thr = cv2mod.get_thr_img(self.freight_crops[0], 200)
        this_year = datetime.datetime.now()
        text = get_text([thr])  # , print_text=True)

        if '배차시간: ' in text:
            text = text.replace('배차시간: ', '')
        elif '배차시간:' in text:
            text = text.replace('배차시간:', '')
        elif '정산시간: ' in text:
            text = text.replace('정산시간: ', '')
        elif '정산시간:' in text:
            text = text.replace('정산시간:', '')
        # print(text)
        date_text = text[:5]

        if text[:2] == '12' and this_year.month == 1:
            load_date = str(this_year.year - 1) + '-' + date_text
        else:
            load_date = str(this_year.year) + '-' + date_text

        result = {'배차시간': load_date+text[5:]}

        return result

    def get_cargo_number(self):
        thr = []
        for crop in self.freight_crops[1:3]:
            thr.append(cv2mod.get_thr_img(crop, 200))
        text = get_text(thr, get_list=True)

        text[1] = text[1].replace('-', '')
        text[1] = list(text[1])
        text[1].insert(1, '-')
        text[1].insert(6, '-')
        text[1] = ''.join(text[1])
        result = {text[0]: text[1]}

        return result

    def get_load_location_info(self):
        thr = cv2mod.get_thr_img(self.freight_crops[3], 200)
        load_location_key = get_text([thr])
        self.load_date, self.load_method = get_load_location_sub_info(self.freight_crops[4])
        thr = cv2mod.get_thr_img(self.freight_crops[4], 200)
        morph = cv2mod.get_morph_img(thr, ker=(3, 5), iterations=4)
        contours = cv2mod.get_contours(morph)
        crops_for_text = cv2mod.get_crops(thr, contours)
        load_location_value = get_text(crops_for_text, lan='kor+eng')
        result = {load_location_key: load_location_value}

        return result

    def get_unload_location_info(self):
        if self.crops_lenth > 15:
            key_crop = self.freight_crops[5]
            value_crop = self.freight_crops[6]
        else:
            key_crop = self.freight_crops[6]
            value_crop = self.freight_crops[7]
        thr = cv2mod.get_thr_img(key_crop, 200)
        unload_location_key = get_text([thr])

        ret1, ret2 = get_unload_location_sub_info(value_crop)
        # print(ret1)
        if ret1 is None:
            xor_img = cv2mod.get_xor_img(value_crop, 150, 250)
            morph_xor = cv2mod.get_morph_img(xor_img, morph_open=False, iterations=1)
            ret1 = get_text([morph_xor])

        self.unload_date = ret1
        self.unload_method = ret2

        thr = cv2mod.get_xor_img(value_crop, 150, 255)
        dilate = cv2mod.get_dilate_img(thr, ker=(12, 23), iterations=1)
        contours = cv2mod.get_contours(dilate)
        crops_for_text = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
        texts = get_text(crops_for_text, lan='kor+eng', get_list=True)

        # print(texts[-1])
        if 'KmM' in texts[-1]:
            distance = int(texts[-1][:-3])
        elif 'Km' or 'km' or 'KM' in texts[-1]:
            distance = (texts[-1][:-2])
        else:
            distance = (texts[-1])+'㎞'
        self.distance = distance

        unload_location_value = ''.join(texts[:-1])
        result = {unload_location_key: unload_location_value}

        return result

    def get_load_unload_date(self):
        result = {'상하차일': f'{self.load_date}/{self.unload_date}'}
        return result

    def get_load_unload_method(self):
        result = {'상하차방법': f'{self.load_method}/{self.unload_method}'}
        return result

    def get_distance(self):
        result = {'거리': self.distance}
        return result

    def get_consoldation(self):
        result = {'혼적': self.consoldation}
        return result

    def get_freight_info(self):
        if self.crops_lenth > 15:
            key_crop = self.freight_crops[7]
            value_crop = self.freight_crops[8]
        else:
            key_crop = self.freight_crops[9]
            value_crop = self.freight_crops[10]

        thr = cv2mod.get_thr_img(key_crop, 220)
        freight_info_key = get_text([thr])

        self.consoldation = get_freight_sub_info(value_crop)

        thr = cv2mod.get_thr_img(value_crop, 180, invert=True)
        dilate = cv2mod.get_dilate_img(thr, ker=(20, 20), iterations=1)
        contours = cv2mod.get_contours(dilate)
        crops_for_text = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
        freight_info_value = get_text(crops_for_text, lan='kor+eng')
        freight_info_value = freight_info_value.replace('ㅅ', 'A')
        freight_info_value = freight_info_value.replace('&', 'A')

        result = {freight_info_key: freight_info_value}

        return result

    def get_quantity(self):
        return {'수량': self.quantity}

    def get_unit(self):
        return {'단위': self.unit}

    def get_truck_class(self):
        if self.crops_lenth > 15:
            return get_dict(self.freight_crops[9:11])
        else:
            return get_dict(self.freight_crops[11:13])

    def get_truck_type(self):
        if self.crops_lenth > 15:
            return get_dict(self.freight_crops[11:13])
        else:
            return get_dict(self.freight_crops[13:])

    def get_load_weight(self):
        return get_dict(self.freight_crops[13:15])

    def get_how_to_trans(self):
        return get_dict(self.freight_crops[15:17])


class ConsignorInfoOCR:
    def __init__(self, consignor_crops):
        print('Run "class ConsignorInfoOCR:"')
        self.consignor_crops = consignor_crops
        self.post_number = None
        # self.show_crops()
        self.consignor_info_dict = self.set_consignor_info_dict()

    def get_dict(self):
        return self.consignor_info_dict

    def set_consignor_info_dict(self):
        print('Run "set_consignor_info_dict(self)"')
        consignor_info_dict = {}
        consignor_info_dict.update(self.get_consignor())
        consignor_info_dict.update(self.get_business_number())
        consignor_info_dict.update(self.get_business_name())
        consignor_info_dict.update(self.get_owner_name())
        consignor_info_dict.update(self.get_business_state())
        consignor_info_dict.update(self.get_business_sector())
        consignor_info_dict.update(self.get_business_address())
        consignor_info_dict.update(self.get_phone_number())
        consignor_info_dict.update(self.get_post_address())
        consignor_info_dict.update(self.get_post_number())
        consignor_info_dict.update(self.get_e_mail())
        
        return consignor_info_dict

    def print_dict(self):
        for keys in self.consignor_info_dict:
            print(f'{keys}: {self.consignor_info_dict[keys]}')
        print()
        
    def show_crops(self):
        i = 0
        for crop in self.consignor_crops:
            cv2.imshow(f'consignor_crops{i}', crop)
            i += 1

    def get_consignor(self):
        return get_dict(self.consignor_crops[0:2])

    def get_business_number(self):
        result = get_dict(self.consignor_crops[2:4])
        result_key = (list(result.keys())[0])
        business_number = result[result_key]
        business_number = business_number.replace('-', '')
        business_number = list(business_number)
        business_number.insert(5, '-')
        business_number.insert(3, '-')
        business_number = ''.join(business_number)
        result[result_key] = business_number

        return result

    def get_business_name(self):
        return get_dict(self.consignor_crops[4:6])

    def get_owner_name(self):
        return get_dict(self.consignor_crops[6:8])

    def get_business_state(self):
        return get_dict(self.consignor_crops[8:10])

    def get_business_sector(self):
        return get_dict(self.consignor_crops[10:12])

    def get_business_address(self):
        result = get_dict(self.consignor_crops[12:14])
        result_key = (list(result.keys())[0])
        address = result[result_key]
        if '(우)' in address:
            address = address[8:]
            address = address.strip()
            result[result_key] = address
        return result

    def get_phone_number(self):
        return get_dict(self.consignor_crops[14:16])

    def get_post_address(self):
        result = get_dict(self.consignor_crops[16:18])
        result_key = (list(result.keys())[0])
        address = result[result_key]
        if '(우)' in address:
            self.post_number = address[3:9]
            address = address[8:]
            address = address.strip()
            result[result_key] = address
        return result

    def get_post_number(self):
        return {'우편번호': self.post_number}

    def get_e_mail(self):
        if len(self.consignor_crops) > 18:
            print(f'len(self.consignor_crops) : {len(self.consignor_crops)}')
            print('Run "get_e_mail(self)"')
            return get_dict(self.consignor_crops[18:20], lan='eng')
        else:
            return {'전자우편': ''}


class PaymentInfoOCR:
    def __init__(self, payment_crops):
        self.payment_crops = payment_crops
        print('<class PaymentInfoOCR> 실행')
        # self.issue_state = '전자발행'
        print(f'len(self.payment_crops) : {len(self.payment_crops)}')
        self.payment_info_dict = self.set_payment_info_dict()

    def get_dict(self):
        return self.payment_info_dict

    def set_payment_info_dict(self):
        payment_info_dict = {}
        payment_info_dict.update(self.get_issue_state())
        payment_info_dict.update(self.get_fare())
        payment_info_dict.update(self.get_commission())
        payment_method = self.get_payment_method()
        payment_info_dict.update(payment_method)
        payment_info_dict.update(self.get_total_amount())
        payment_info_dict.update(self.get_collect_state())
        payment_info_dict.update(self.get_invoice_issue_state(payment_method))
        
        return payment_info_dict

    def print_dict(self):
        for keys in self.payment_info_dict:
            print(f'{keys}: {self.payment_info_dict[keys]}')
        print()

    def show_crops(self):
        i = 0
        for crop in self.payment_crops:
            cv2.imshow(f'payment_crops{i}', crop)
            i += 1

    def get_issue_state(self):
        issue_state = get_text([self.payment_crops[-1]])
        # cv2.imshow('get_issue_state', self.payment_crops[0])
        if issue_state == '미발행상태':
            return {'전자세금계산서': issue_state}
        else:
            return {'전자세금계산서': '전자발행'}

    def get_fare(self):
        return get_dict(self.payment_crops[2:4])

    def get_commission(self):
        return get_dict(self.payment_crops[4:6])

    def get_payment_method(self):
        return get_dict(self.payment_crops[6:8])

    def get_total_amount(self):
        return get_dict(self.payment_crops[8:10])

    def get_collect_state(self):
        return get_dict(self.payment_crops[10:12])

    def get_invoice_issue_state(self, payment_method):
        print('Run "get_invoice_issue_state(self)"')
        print(f'payment_method : {payment_method}')
        if len(self.payment_crops) >= 19:
            return get_dict(self.payment_crops[14:16])
        elif len(self.payment_crops) == 14:
            return get_dict(self.payment_crops[12:16])


def get_dict(crops_for_text, lan='kor'):
    key_text = get_key_text(crops_for_text[0])
    value_text = get_multi_line_text(crops_for_text[1], lan)

    return {key_text: value_text}


def get_multi_line_text(crop_for_text, lan):
    thr = cv2mod.get_thr_img(crop_for_text, 180, invert=True)
    dilate = cv2mod.get_dilate_img(thr, ker=(20, 20), iterations=1)
    contours = cv2mod.get_contours(dilate)
    crops_for_text = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)

    return get_text(crops_for_text, lan=lan)


def get_key_text(crop_for_key_text):
    thr = cv2mod.get_thr_img(crop_for_key_text, 200, invert=True)
    dilate = cv2mod.get_dilate_img(thr, ker=(20, 20), iterations=1)
    contours = cv2mod.get_contours(dilate)
    crops_for_text = cv2mod.get_crops(thr, contours, invert=True)
    # cv2.imshow('get_key_text', crop_for_text)
    result = get_text(crops_for_text, psm=7)  # , print_text=True)

    return result


def get_text(crops_for_text, lan='kor', psm=7, print_text=False, get_list=False):
    texts = []
    psm_config = f'--psm {psm}'

    for crop in crops_for_text:
        text = pytesseract.image_to_string(crop, lang=lan, config=psm_config)
        if print_text:
            print(list(text))
        texts.append(text.strip('\n'))

    if get_list:
        result = texts
    else:
        result = ''.join(texts)
    return result


def get_load_location_sub_info(src):
    thr = cv2mod.get_thr_img(src, 190, invert=True)  # , invert=True)
    contours = cv2mod.get_contours(thr)

    img_name = ['사인', '당상', '내상', '지', '수']
    sub_info_list = []
    icons = get_load_location_icons()

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            crop = src[y:y + h, x:x + w].copy()
            j = 0
            for icon in icons:
                # print(img_list[j].shape)
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(crop, dsize=(icon_height, icon_width))
                img_add = cv2.bitwise_or(resize_crop, icon)

                if int(np.mean(img_add)) > 240:
                    sub_info_list.append(img_name[j])
                    cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)
                j += 1

    ret1 = None
    ret2 = None

    for sub_info in sub_info_list:
        if sub_info == '당상' or sub_info == '내상':
            ret1 = sub_info
        elif sub_info == '지' or sub_info == '수':
            ret2 = sub_info

    return ret1, ret2


def get_unload_location_sub_info(src):
    img_name = ['사인', '월착', '당착', '내착', '지', '수']
    icons = get_unload_location_icons()

    thr = cv2mod.get_thr_img(src, 190, invert=True)
    contours = cv2mod.get_contours(thr)
    sub_info_list = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            crop = src[y:y + h, x:x + w].copy()
            j = 0
            for icon in icons:
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(crop, dsize=(icon_height, icon_width))
                img_add = cv2.bitwise_or(resize_crop, icon)

                if int(np.mean(img_add)) > 240:
                    sub_info_list.append(img_name[j])
                    cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)
                j += 1

    ret1 = None
    ret2 = None

    for sub_info in sub_info_list:
        if sub_info == '당착' or sub_info == '내착' or sub_info == '월착':
            ret1 = sub_info
        elif sub_info == '지' or sub_info == '수':
            ret2 = sub_info

    return ret1, ret2


def get_load_location_icons():
    result = [cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_sign.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_load_today.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_load_tomorrow.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_handwork.png', cv2.IMREAD_GRAYSCALE)]

    return result


def get_unload_location_icons():
    result = [cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_sign.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_monday.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_today.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_tomorrow.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_fork_lift.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_handwork.png',
                         cv2.IMREAD_GRAYSCALE)]

    return result


def get_freight_sub_info(src):
    img_name = ('혼적', '독차', '예약')
    icons = get_freight_info_icons()

    thr = cv2mod.get_thr_img(src, 200, invert=True)
    morph = cv2mod.get_morph_img(thr, ker=(5, 5), morph_open=False, iterations=1)
    contours = cv2mod.get_contours(morph)

    sub_info_list = []

    for cnt in contours:

        if 500 < cv2.contourArea(cnt):
            x, y, w, h = cv2.boundingRect(cnt)
            crop = src[y:y + h, x:x + w]

            j = 0
            for icon in icons:
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(crop, dsize=(icon_height, icon_width))
                img_add = cv2.bitwise_xor(resize_crop, icon)

                if int(np.mean(img_add)) > 230:
                    sub_info_list.append(img_name[j])
                    cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)
                j += 1

    result = None

    for sub_info in sub_info_list:
        if sub_info == '혼적' or sub_info == '독차':
            result = sub_info

    return result


def get_freight_info_icons():
    result = [
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_consoldation.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_in_full.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_reservation.png', cv2.IMREAD_GRAYSCALE)]
    return result


if __name__ == '__main__':
    # file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/old/'
    # files = ['dr_2022-03-26_150504.png', 'dr_2022-03-26_150505.png', 'dr_2022-03-26_150507.png']
    # file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/old/'
    file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/'
    # files = ['dr_2022-03-26_150504.png', 'dr_2022-03-26_150505.png', 'dr_2022-03-26_150507.png']
    files = ['dr_2022-06-20_183249.png', 'dr_2022-06-20_183253.png', 'dr_2022-06-20_183253.png']

    crops = MakeCrop.make_crops(file_path, files)

    freightInfoOCR = FreightInfoOCR(crops[0])
    consignorInfoOCR = ConsignorInfoOCR(crops[1])
    paymentInfoOCR = PaymentInfoOCR(crops[2])

    freightInfoOCR.print_dict()
    consignorInfoOCR.print_dict()
    paymentInfoOCR.print_dict()

    freightInfoOCR.show_crops()
    consignorInfoOCR.show_crops()
    paymentInfoOCR.show_crops()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
