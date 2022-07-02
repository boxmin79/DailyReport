import cv2
import numpy as np
import cv2Mod
from easyocr import Reader


class MakeCrops:
    def __init__(self, image_file_path, image_file_list):
        print("<class 'MakeCrops'>를 실행합니다.")
        self.filePath = image_file_path
        self.fileNameList = image_file_list
        print(f'File Path : {self.filePath}')

        idx = 0
        for file_name in self.fileNameList:
            print(f'File[{idx}] = {self.filePath}{file_name}')
            idx += 1

        print('이미지파일을 Grayscale로 읽습니다.')
        self.freight_image = cv2.imread(self.filePath + self.fileNameList[0], cv2.IMREAD_GRAYSCALE)
        self.consignor_image = cv2.imread(self.filePath + self.fileNameList[1], cv2.IMREAD_GRAYSCALE)
        self.payment_image = cv2.imread(self.filePath + self.fileNameList[2], cv2.IMREAD_GRAYSCALE)

        # cv2.imshow('MakeCrops.freight_image', self.freight_image)
        # cv2.imshow('MakeCrops.consignor_image', self.consignor_image)
        # cv2.imshow('MakeCrops.payment_image', self.payment_image)

    def get_freight(self):
        # 전자세금 계산서 '미발행상태' crop
        get_text_iti(self.freight_image)
        # 전화마크 'A'마크 지우기
        get_del_phone_and_a(self.freight_image, 2000, 6000)  # 2000, 6000
        # 글자 지우기
        del_text_area = get_del_text_area(self.freight_image)
        # 데이터영역 표시
        draw_data_area = get_draw_data_area(del_text_area)
        # 데이터영역 외곽선(contours 가져오기
        data_area_contours = get_data_area_contours(draw_data_area)
        # 데이터 영역 조각리스트 가져오기
        return cv2Mod.get_crops(self.freight_image, data_area_contours,
                                invert=False, contours_reverse=True, draw_rect=True)

    def get_consignor(self):
        # 세금계산서 발행여부
        get_text_iti(self.consignor_image)
        # 전화 아이콘 A아이콘 지우기
        get_del_phone_and_a(self.consignor_image, 2000, 6000)  # 2000, 6000
        # 글자 지우기
        del_text_area = get_del_text_area(self.consignor_image)
        # 외곽선 가져오기
        data_area_contours = get_data_area_contours(del_text_area, freight_img=False)
        # 이미지 조각 가져오기
        return cv2Mod.get_crops(self.consignor_image, data_area_contours, invert=False, contours_reverse=True)

    def get_payment(self):
        # 세금계산서 발행 Crop
        text_iti = get_text_iti(self.payment_image)
        # '전화' & 'A' 아이콘 지우기
        get_del_phone_and_a(self.payment_image, 6000, 10000)  # 6000 10000
        # 글자 지우기
        del_text_area = get_del_text_area(self.payment_image)
        # 외곽선 가져오기
        data_area_contours = get_data_area_contours(del_text_area, freight_img=False)
        # 이미지 조각 가져오기
        crops_for_texts = cv2Mod.get_crops(self.payment_image, data_area_contours, invert=False, contours_reverse=True)
        return crops_for_texts + text_iti

    def image_preprocessing(self):
        pass


# 전화기 A 마크 지우기
def get_del_phone_and_a(consignor_src, min_area, max_area):
    thr = cv2Mod.get_thr_img(consignor_src, 250, invert=True)
    contours = cv2Mod.get_contours(thr, retr='ccomp')
    # i = 0
    for cnt in contours:
        if min_area < cv2.contourArea(cnt) < max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.9 < w / h < 1.1:
                cv2.rectangle(consignor_src, (x, y), (x + w, y + h), 255, cv2.FILLED)


# 데이터 영역 그리기
def get_data_area_contours(data_area, freight_img=True):
    if freight_img:
        contours = cv2Mod.get_contours(data_area, retr='list')[:-2]
        if len(contours) == 20:
            result = contours[:10] + contours[11:-2]
        else:
            result = contours[:6] + contours[7:-2]
    else:
        thr = cv2Mod.get_thr_img(data_area, 230, invert=True)
        morph = cv2Mod.get_morph_img(thr, ker=(3, 3), morph_open=False, iterations=1, invert=False)
        contours = cv2Mod.get_contours(morph, retr='list')[:-2]
        result = contours[:-1]
    return result


# get_draw_data_area
def get_draw_data_area(del_text_area):
    thr_xor = cv2Mod.get_xor_img(del_text_area, 220, 230, invert=True)
    contours = cv2Mod.get_contours(thr_xor, retr="ccomp")

    for cnt in contours[1:]:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(del_text_area, (x, y), (x + w, y + h), 0, 1)

    x0, y0, w0, h0 = cv2.boundingRect(contours[0])
    if len(contours) == 20:
        x2, y2, w2, h2 = cv2.boundingRect(contours[18])
    else:
        x2, y2, w2, h2 = cv2.boundingRect(contours[16])
    cv2.rectangle(del_text_area, (x0, y2 + h2), (x0 + w0, y0), 0, 1)
    return del_text_area


# 글자 지우는 함수
def get_del_text_area(img_src):
    del_text_area = img_src.copy()
    thr = cv2Mod.get_thr_img(img_src, 223, invert=True)  # 223
    dilate = cv2Mod.get_dilate_img(thr, ker=(3, 3), iterations=2, dilate=True)
    contours = cv2Mod.get_contours(dilate, retr="ccomp")

    for cnt in contours:
        cv2.drawContours(del_text_area, [cnt], 0, (255, 255, 255), cv2.FILLED, cv2.LINE_8)
    
    return del_text_area


# 전자세금 계산서 '미발행상태' 출력 함수
def get_text_iti(img_src):
    result = []
    thr_xor = cv2Mod.get_xor_img(img_src, 220, 230)
    morph = cv2Mod.get_morph_img(thr_xor, ker=(3, 3), morph_open=False, iterations=2, invert=True)
    contours = cv2Mod.get_contours(morph)

    if len(contours) > 0:
        iti_crops = cv2Mod.get_crops(img_src, contours)
        cv2Mod.del_area(img_src, contours)
        xor_crop = cv2Mod.get_xor_img(iti_crops[0], 100, 160, invert=True)
        morph = cv2Mod.get_morph_img(xor_crop, ker=(3, 3), morph_open=True, iterations=1)
        contours_for_text = cv2Mod.get_contours(morph, retr="external")
        if len(contours_for_text) > 0:
            result = cv2Mod.get_crops(xor_crop, contours_for_text, draw_rect=True)  # , invert=True)
    return result


# 화물정보 아이콘 가져오기
def get_freight_info_icons():
    icon_path = 'C:/Users/realb/PycharmProjects/DailyReport/img/'
    result = [
        cv2.imread(icon_path+'img_consoldation.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread(icon_path+'img_in_full.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread(icon_path+'img_reservation.png', cv2.IMREAD_GRAYSCALE)]
    return result


# 상차지 아이콘 가져오기
def get_load_location_icons():
    icon_path = 'C:/Users/realb/PycharmProjects/DailyReport/img/'
    result = [cv2.imread(icon_path+'img_sign.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread(icon_path+'img_load_today.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread(icon_path+'img_load_tomorrow.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread(icon_path+'img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread(icon_path+'img_handwork.png', cv2.IMREAD_GRAYSCALE)]

    return result


# 하차지 아이콘 가져오기
def get_unload_location_icons():
    icon_path = 'C:/Users/realb/PycharmProjects/DailyReport/img/'
    return [cv2.imread(icon_path+'img_sign.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread(icon_path+'img_arrive_monday.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread(icon_path+'img_arrive_today.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread(icon_path+'img_arrive_tomorrow.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread(icon_path+'img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
            cv2.imread(icon_path+'img_handwork.png', cv2.IMREAD_GRAYSCALE)]


# 화물 서브 정보
def get_freight_sub_info(src):
    img_name = ['혼적', '독차', '예약']
    icons = get_freight_info_icons()

    thr = cv2Mod.get_thr_img(src, 200, invert=True)
    morph = cv2Mod.get_morph_img(thr, ker=(5, 5), morph_open=False, iterations=1)
    contours = cv2Mod.get_contours(morph)

    sub_info_list = []

    for cnt in contours:

        if 500 < cv2.contourArea(cnt):
            x, y, w, h = cv2.boundingRect(cnt)
            sub_info_crop = src[y:y + h, x:x + w]

            j = 0
            for icon in icons:
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(sub_info_crop, dsize=(icon_height, icon_width))
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


# 하차지 서브 정보
def get_unload_location_sub_info(src):
    img_name = ['사인', '월착', '당착', '내착', '지', '수']
    icons = get_unload_location_icons()

    thr = cv2Mod.get_thr_img(src, 190, invert=True)
    contours = cv2Mod.get_contours(thr)
    sub_info_list = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            sub_info_crop = src[y:y + h, x:x + w].copy()
            j = 0
            for icon in icons:
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(sub_info_crop, dsize=(icon_height, icon_width))
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


# 상차지 서브 정보
def get_load_location_sub_info(src):
    thr = cv2Mod.get_thr_img(src, 190, invert=True)  # , invert=True)
    contours = cv2Mod.get_contours(thr)

    img_name = ['사인', '당상', '내상', '지', '수']
    sub_info_list = []
    icons = get_load_location_icons()

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            sub_info_crop = src[y:y + h, x:x + w].copy()
            j = 0
            for icon in icons:
                # print(img_list[j].shape)
                icon_width, icon_height = icon.shape
                resize_crop = cv2.resize(sub_info_crop, dsize=(icon_height, icon_width))
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


if __name__ == "__main__":
    # file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/'
    file_path = r'D:/dr_img_backup/'
    # files = ['dr_2022-03-26_150504.png', 'dr_2022-03-26_150505.png', 'dr_2022-03-26_150507.png']
    files = ['dr_2022-06-20_183326.png', 'dr_2022-06-20_183329.png', 'dr_2022-06-20_183332.png']

    makeCrops = MakeCrops(file_path, files)
    freightCrops = makeCrops.get_freight()
    print(len(freightCrops))
    i = 0
    # for crop in freightCrops:
    #     cv2.imshow(f'freightCrops[{i}]', crop)
    #     i += 1
    langs = ['ko', 'en']
    reader = Reader(lang_list=langs, gpu=False)
    for crop in freightCrops:
        cv2.imshow(f'freightCrops[{i}]', crop)
        result = reader.readtext(crop)
        print(result)
        i += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()
