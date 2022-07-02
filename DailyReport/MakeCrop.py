import cv2
import numpy as np
import cv2mod


def make_crops(image_file_path, file_names):
    image_list = []
    for file_name in file_names:
        image_list.append(cv2.imread(image_file_path + file_name, cv2.IMREAD_GRAYSCALE))

    freight_crops = freight_crops_func(image_list[0])
    consignor_crops = consignor_crops_func(image_list[1])
    payment_crops = payment_crops_func(image_list[2])

    return freight_crops, consignor_crops, payment_crops


def freight_crops_func(freight_src):
    # 전자세금 계산서 '미발행상태' crop
    get_text_iti(freight_src)

    get_del_phone_and_a(freight_src)
    # cv2.imshow('get_del_phone_and_a', freight_src)

    # 글자 지우기
    del_text_area = get_del_text_area(freight_src)
    # cv2.imshow('del_text_area', del_text_area)

    # 데이터영역 표시
    draw_data_area = get_draw_data_area(del_text_area)
    # cv2.imshow('test', draw_data_area)

    # 데이터영역 외곽선 가져오기
    data_area_contours = get_data_area_contours(draw_data_area)

    # 데이터 영역 조각리스트
    crops_for_text = cv2mod.get_crops(freight_src, data_area_contours,
                                      invert=False, contours_reverse=True, draw_rect=True)
    # print(type(data_area_crop_list))
    # i = 0
    # for crop in data_area_crop_list:
    #     cv2.imshow(f'{i}', crop)
    #     i += 1

    result = crops_for_text

    return result


def consignor_crops_func(consignor_src):
    # 세금계산서 발행여부
    get_text_iti(consignor_src)

    # 전화 아이콘 A아이콘 지우기
    get_del_phone_and_a(consignor_src)

    # 글자 지우기
    del_text_area = get_del_text_area(consignor_src)

    # 외곽선 가져오기
    data_area_contours = get_data_area_contours(del_text_area, freight_img=False)

    # 이미지 조각 가져오기
    crops_for_text = cv2mod.get_crops(consignor_src, data_area_contours, invert=False, contours_reverse=True)

    result = crops_for_text

    return result


def payment_crops_func(payment_src):
    text_iti = get_text_iti(payment_src)
    # print(text_iti)

    get_del_icon(payment_src)

    del_text_area = get_del_text_area(payment_src)
    # cv2.imshow('del_text_area', del_text_area)

    data_area_contours = get_data_area_contours(del_text_area, freight_img=False)
    # print(len(data_area_contours))

    crops_for_texts = cv2mod.get_crops(payment_src, data_area_contours, invert=False, contours_reverse=True)

    result = crops_for_texts + text_iti

    return result


def get_del_icon(payment_src):
    thr = cv2mod.get_thr_img(payment_src, 250, invert=True)
    contours = cv2mod.get_contours(thr, retr='ccomp')

    for cnt in contours:
        if 6000 < cv2.contourArea(cnt) < 10000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(payment_src, (x, y), (x + w, y + h), 255, cv2.FILLED)


# 전화기 A 마크 지우기
def get_del_phone_and_a(consignor_src):
    thr = cv2mod.get_thr_img(consignor_src, 250, invert=True)
    contours = cv2mod.get_contours(thr, retr='ccomp')
    # i = 0
    for cnt in contours:
        if 2000 < cv2.contourArea(cnt) < 6000:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.9 < w / h < 1.1:
                cv2.rectangle(consignor_src, (x, y), (x + w, y + h), 255, cv2.FILLED)


# 데이터 영역 그리기
def get_data_area_contours(data_area, freight_img=True):
    if freight_img:
        contours = cv2mod.get_contours(data_area, retr='list')[:-2]
        if len(contours) == 20:
            result = contours[:10] + contours[11:-2]
        else:
            result = contours[:6] + contours[7:-2]
        # print(len(result))
        # cv2.imshow('get_data_area_contours, True', data_area)
    else:
        thr = cv2mod.get_thr_img(data_area, 230, invert=True)
        morph = cv2mod.get_morph_img(thr, ker=(3, 3), morph_open=False, iterations=1, invert=False)
        # cv2.imshow('get_data_area_contours, thr', morph)
        contours = cv2mod.get_contours(morph, retr='list')[:-2]
        result = contours[:-1]

        # cv2.imshow('get_data_area_contours, false', data_area)

        # i = 0
        for cnt in result:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(data_area, (x, y), (x + w, y + h), 0, 1)
            # cv2.putText(data_area, str(i), tuple(cnt[0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.8, 0, 1)
            # i += 1
    # cv2.imshow('get_data_area_contours', data_area)

    return result


# get_draw_data_area
def get_draw_data_area(del_text_area):
    # thr_xor = cv2mod.get_xor_img(del_text_area, 240, 250)
    thr_xor = cv2mod.get_xor_img(del_text_area, 220, 230, invert=True)
    # cv2.imshow('get_draw_data_area', thr_xor)
    # morph = cv2mod.get_morph_img(thr_xor, ker=(35, 5), morph_open=True, iterations=1, invert=True)
    # cv2.imshow('get_draw_data_area', morph)
    # thr = cv2mod.get_thr_img(del_text_area, 250, invert=True)
    # thr_or = cv2.bitwise_or(thr, morph)
    contours = cv2mod.get_contours(thr_xor, retr="ccomp")
    # print(len(contours))

    # i = 0
    for cnt in contours[1:]:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(del_text_area, (x, y), (x + w, y + h), 0, 1)
        # cv2.putText(del_text_area, str(i), tuple(cnt[0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.8, 0, 1)
        # i += 1

    x0, y0, w0, h0 = cv2.boundingRect(contours[0])
    if len(contours) == 20:
        x2, y2, w2, h2 = cv2.boundingRect(contours[18])
    else:
        x2, y2, w2, h2 = cv2.boundingRect(contours[16])
    cv2.rectangle(del_text_area, (x0, y2 + h2), (x0 + w0, y0), 0, 1)

    # cv2.imshow('get_draw_data_area', del_text_area)

    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(del_text_area, (x, y), (x + w, y + h), 0, 1)

    return del_text_area


# 글자 지우는 함수
def get_del_text_area(img_src):
    del_text_area = img_src.copy()
    thr = cv2mod.get_thr_img(img_src, 223, invert=True)  # 223
    dilate = cv2mod.get_dilate_img(thr, ker=(3, 3), iterations=2, dilate=True)
    contours = cv2mod.get_contours(dilate, retr="ccomp")

    for cnt in contours:
        cv2.drawContours(del_text_area, [cnt], 0, (255, 255, 255), cv2.FILLED, cv2.LINE_8)
    # cv2.imshow('get_del_text_area', del_text_area)
    return del_text_area


# 전자세금 계산서 '미발행상태' 출력 함수
def get_text_iti(img_src):
    result = []
    thr_xor = cv2mod.get_xor_img(img_src, 220, 230)
    # cv2.imshow('get_text_iti', thr_xor)
    morph = cv2mod.get_morph_img(thr_xor, ker=(3, 3), morph_open=False, iterations=2, invert=True)
    contours = cv2mod.get_contours(morph)

    if len(contours) > 0:
        crops = cv2mod.get_crops(img_src, contours)
        cv2mod.del_area(img_src, contours)
        xor_crop = cv2mod.get_xor_img(crops[0], 100, 160, invert=True)
        morph = cv2mod.get_morph_img(xor_crop, ker=(3, 3), morph_open=True, iterations=1)
        # cv2.imshow('get_text_iti', morph)
        contours_for_text = cv2mod.get_contours(morph, retr="external")
        if len(contours_for_text) > 0:
            result = cv2mod.get_crops(xor_crop, contours_for_text, draw_rect=True)  # , invert=True)
            # cv2.imshow('get_text_iti', result[0])
    # i = 0
    # for re in result:
    #     cv2.imshow(f'get_text_iti{i}', re)
    #     i += 1
    return result


# 화물정보 아이콘 가져오기
def get_freight_info_icons():
    result = [
        cv2.imread('/img/img_consoldation.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('/img/img_in_full.png', cv2.IMREAD_GRAYSCALE),
        cv2.imread('/img/img_reservation.png', cv2.IMREAD_GRAYSCALE)]
    return result


# 상차지 아이콘 가져오기
def get_load_location_icons():
    result = [cv2.imread('/img/img_sign.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_load_today.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_load_tomorrow.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_fork_lift.png', cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_handwork.png', cv2.IMREAD_GRAYSCALE)]

    return result


# 하차지 아이콘 가져오기
def get_unload_location_icons():
    result = [cv2.imread('/img/img_sign.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_arrive_monday.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_arrive_today.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_arrive_tomorrow.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_fork_lift.png',
                         cv2.IMREAD_GRAYSCALE),
              cv2.imread('/img/img_handwork.png',
                         cv2.IMREAD_GRAYSCALE)]

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


if __name__ == "__main__":
    # file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/old/'
    # files = ['dr_2022-03-26_150450.png', 'dr_2022-03-26_150452.png', 'dr_2022-03-26_150453.png']

    # file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/old/'
    file_path = r'/img/dr/'
    # files = ['dr_2022-03-26_150504.png', 'dr_2022-03-26_150505.png', 'dr_2022-03-26_150507.png']
    files = ['dr_2022-06-20_183249.png', 'dr_2022-06-20_183253.png', 'dr_2022-06-20_183253.png']

    crops = make_crops(file_path, files)

    # i = 0
    # for crop in crops[0]:
    #     cv2.imshow(f'test({i})', crop)
    #     i += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()
