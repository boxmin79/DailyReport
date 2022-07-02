import cv2
import numpy as np
import cv2mod
import datetime
from datetime import date
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'c:/Program Files/Tesseract-OCR/tesseract'


def freight_info_sector(src):
    result = []
    # 전자세금 계산서 '미발행상태' 출력 함수
    text_iti = get_text_iti(src)

    # 글자 지우기
    del_text_area = get_del_text_area(src)

    # 데이터영역 표시
    draw_data_area = get_draw_data_area(del_text_area)

    # 데이터영역 외곽선 가져오기
    data_area_contours = get_data_area_contours(draw_data_area)

    # 데이터 영역 조각리스트
    data_area_crop_list = cv2mod.get_crops(src, data_area_contours, invert=False, contours_reverse=True, draw_rect=True)

    # 배차시간 data_area_crop_list[0]
    load_date = get_load_date(data_area_crop_list[0])
    load_date = date.fromisoformat(load_date)
    result.append(load_date)

    # 화물번호 data_area_crop_list[1]
    cargo_number = get_cargo_number(data_area_crop_list[1])
    result.append(cargo_number)

    # 상차지 텍스트화
    load_loc, load_day, load_method = get_load_location_info(data_area_crop_list[2])
    result.append(load_loc)

    # 하차지 텍스트화
    unload_loc, unload_day, unload_method, distance = get_unload_location_info(data_area_crop_list[3])
    result.append(unload_loc)
    result.append(distance)
    result.append(f'{load_day}/{unload_day}')
    result.append(f'{load_method}/{unload_method}')

    # 화물정보
    freight_info, consoldation = get_freight_info(data_area_crop_list[4])
    result.append(freight_info)
    result.insert(len(result) - 1, consoldation)

    # 톤수
    truck_class = get_truck_class(data_area_crop_list[5])
    result.append(truck_class)

    # 차종
    truck_type = get_truck_type(data_area_crop_list[6])
    result.append(truck_type)

    # 적재중량
    load_weight = get_load_weight(data_area_crop_list[7])
    result.append(load_weight)

    # 운행방법
    how_to_trans = get_how_to_trans(data_area_crop_list[8])
    result.append(how_to_trans)

    return result


# 운행방법
def get_how_to_trans(src):
    thr = cv2mod.get_thr_img(src, 240)
    result = get_text([thr])

    return result


# 적재중량
def get_load_weight(src):
    thr = cv2mod.get_thr_img(src, 240)
    result = get_text([thr])

    return result


# 차종
def get_truck_type(src):
    thr = cv2mod.get_thr_img(src, 240)
    result = get_text([thr])

    return result


# 트럭 톤수(급)
def get_truck_class(src):
    thr = cv2mod.get_thr_img(src, 240)
    result = get_text([thr])

    return result


# 화물정보 텍스트화
def get_freight_info(src):
    ret1 = get_freight_sub_info(src)

    thr = cv2mod.get_thr_img(src, 180, invert=True)
    dilate = cv2mod.get_dilate_img(thr, ker=(20, 20), iterations=1)
    contours = cv2mod.get_contours(dilate)
    crops = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
    text = get_text(crops, lan='kor+eng')
    result = text
    result = result.replace('ㅅ', 'A')
    result = result.replace('&', 'A')

    return result, ret1


# 하차지 텍스트화 함수
def get_unload_location_info(src):
    ret1, ret2 = get_unload_location_sub_info(src)
    # print(ret1)
    if ret1 is None:
        xor_img = cv2mod.get_xor_img(src, 150, 250)
        morph_xor = cv2mod.get_morph_img(xor_img, morph_open=False, iterations=1)
        ret1 = get_text([morph_xor])

    thr = cv2mod.get_xor_img(src, 150, 255)
    dilate = cv2mod.get_dilate_img(thr, ker=(12, 23), iterations=1)
    contours = cv2mod.get_contours(dilate)
    crops = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
    texts = get_text(crops, lan='kor+eng', get_list=True)

    # print(texts[-1])
    if 'KmM' in texts[-1]:
        distance = int(texts[-1][:-3])
    elif 'Km' or 'km' or 'KM' in texts[-1]:
        distance = int(texts[-1][:-2])
    else:
        distance = int(texts[-1])
    result = ''.join(texts[:-1])

    return result, ret1, ret2, distance


# 상차지 텍스트화 함수
def get_load_location_info(src):
    ret1, ret2 = get_load_location_sub_info(src)
    thr = cv2mod.get_thr_img(src, 200)
    morph = cv2mod.get_morph_img(thr, ker=(3, 5), iterations=4)
    contours = cv2mod.get_contours(morph)
    crops = cv2mod.get_crops(thr, contours)
    result = get_text(crops)

    return result, ret1, ret2


# 화물번호 텍스트화
def get_cargo_number(src):
    thr = cv2mod.get_thr_img(src, 200) # 100
    text = get_text([thr])
    text = text.replace('-', '')
    text = list(text)
    text.insert(1, '-')
    text.insert(6, '-')
    result = ''.join(text)

    return result


# 배차시간 텍스트화 함수
def get_load_date(src):
    thr = cv2mod.get_thr_img(src, 200)
    this_year = datetime.datetime.now()
    text = get_text([thr])#, print_text=True)

    if '배차시간: ' in text:
        text = text.replace('배차시간: ', '')
    elif '배차시간:' in text:
        text = text.replace('배차시간:', '')
    elif '정산시간: ' in text:
        text = text.replace('정산시간: ', '')
    elif '정산시간:' in text:
        text = text.replace('정산시간:', '')

    text = text[:5]

    if text[:2] == '12' and this_year.month == 1:
        result = str(this_year.year - 1) + '-' + text
    else:
        result = str(this_year.year) + '-' + text

    return result

# 글씨 가져올 부분 조각내기는 함수
# def get_data_area_crop_list(contours, src):
#     result = []
#
#     for cnt in reversed(contours):
#         x, y, w, h = cv2.boundingRect(cnt)
#         cv2.rectangle(src, (x, y), (x + w, y + h), 255, 5)
#         result.append(src[y:y + h, x:x + w])
#
#     return result


# 데이터 영역 그리기
def get_data_area_contours(draw_data_area):
    black = np.zeros_like(draw_data_area)
    thr = cv2mod.get_thr_img(draw_data_area, 250)
    morph = cv2mod.get_morph_img(thr, ker=(36, 5), invert=True)
    contours = cv2mod.get_contours(morph, retr='ccomp')[1:]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(black, (x, y), (x + w, y + h), 255, 1)

    return contours


# get_draw_data_area
def get_draw_data_area(del_text_area):
    thr_xor = cv2mod.get_xor_img(del_text_area, 240, 250)
    morph = cv2mod.get_morph_img(thr_xor, ker=(35, 5), morph_open=True, iterations=1, invert=True)
    thr = cv2mod.get_thr_img(del_text_area, 250, invert=True)
    thr_or = cv2.bitwise_or(thr, morph)
    contours = cv2mod.get_contours(thr_or)

    x0, y0, w0, h0 = cv2.boundingRect(contours[0])
    x2, y2, w2, h2 = cv2.boundingRect(contours[1])
    cv2.rectangle(del_text_area, (x0, y2 + h2), (x0 + w0, y0), 0, 1)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(del_text_area, (x, y), (x + w, y + h), 0, 1)

    return del_text_area


# 글자 지우는 함수
def get_del_text_area(src):
    del_text_area = src.copy()
    thr = cv2mod.get_thr_img(src, 223, invert=True)  # 223
    dilate = cv2mod.get_dilate_img(thr, ker=(3, 3), iterations=2, dilate=True)
    contours = cv2mod.get_contours(dilate, retr="ccomp")

    for cnt in contours:
        cv2.drawContours(del_text_area, [cnt], 0, (255, 255, 255), cv2.FILLED, cv2.LINE_8)

    return del_text_area


# 전자세금 계산서 '미발행상태' 출력 함수
def get_text_iti(src):
    result = None
    thr_xor = cv2mod.get_xor_img(src, 220, 230)
    morph = cv2mod.get_morph_img(thr_xor, ker=(3, 3), morph_open=False, iterations=2, invert=True)
    contours = cv2mod.get_contours(morph)

    if len(contours) > 0:
        crops = cv2mod.get_crops(src, contours)
        cv2mod.del_area(src, contours)
        xor_crop_for_text = cv2mod.get_xor_img(crops[0], 100, 160, invert=True)
        morph_for_text = cv2mod.get_morph_img(xor_crop_for_text, ker=(3, 3), morph_open=False, iterations=2)
        contours_for_text = cv2mod.get_contours(morph_for_text, retr="external")
        if len(contours_for_text) > 0:
            crops_for_text = cv2mod.get_crops(xor_crop_for_text, contours_for_text, invert=True)
            result = get_text(crops_for_text, psm=6)#, print_text=True)

    return result


# 이미지를 글자로 바꿔주는 함수
def get_text(crops, lan='kor', psm=7, print_text=False, get_list=False):
    texts = []
    psm_config = f'--psm {psm}'

    for crop in crops:
        text = pytesseract.image_to_string(crop, lang=lan, config=psm_config)
        if print_text:
            print(list(text))
        texts.append(text.strip('\n'))
    if get_list:
        result = texts
    else:
        result = ''.join(texts)
    return result


# 화물정보 아이콘 가져오기
def get_freight_info_icons():
    result = [
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_consoldation.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_in_full.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_reservation.png', cv2.IMREAD_GRAYSCALE)]
    return result


# 상차지 아이콘 가져오기
def get_load_location_icons():
    result = [cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_sign.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_load_today.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_load_tomorrow.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_handwork.png', cv2.IMREAD_GRAYSCALE)]

    return result


# 하차지 아이콘 가져오기
def get_unload_location_icons():
    result = [cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_sign.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_monday.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_today.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_arrive_tomorrow.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('C:/Users/realb/PycharmProjects/DailyReport/img/img_handwork.png', cv2.IMREAD_GRAYSCALE)]

    return result


# 화물 서브 정보
def get_freight_sub_info(src):
    img_name = ['혼적', '독차', '예약']
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


# 하차지 서브 정보
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


# 상차지 서브 정보
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


# file_path = r''C:/Users/realb/PycharmProjects/DailyReport/img/dr/'
# file = 'dr_2022-03-26_150450.png'
# file = 'dr_2022-03-27_171822.png'
# for i in range(0,len(file_list),3):
#     src = cv2.imread(file_path + file_list[i], cv2.IMREAD_GRAYSCALE)
#     print(f'=============파일번호({i})=============')
#     freight_info_sector(src)
#     print()

# gray = cv2.imread(file_path + file, cv2.IMREAD_GRAYSCALE)
# freight_info_sector(gray)
#
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
