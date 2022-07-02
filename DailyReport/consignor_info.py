import cv2
import numpy as np
import pytesseract
import cv2mod

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract'


def get_consignor_info(src):
    result = []
    # 세금계산서 발행여부
    text_iti = get_text_iti(src)

    # 전화 아이콘 A아이콘 지우기
    get_del_phone_and_a(src)

    # 글자 지우기
    del_text_area = get_del_text_area(src)

    # 외곽선 가져오기
    data_area_contours = get_data_area_contours(del_text_area)

    # 이미지 조각 가져오기
    crops_for_text = cv2mod.get_crops(src, data_area_contours, invert=False, contours_reverse=True)

    for crop_for_text in crops_for_text:
        thr = cv2mod.get_thr_img(crop_for_text, 180, invert=True)
        dilate = cv2mod.get_dilate_img(thr, ker=(20, 20), iterations=1)
        contours = cv2mod.get_contours(dilate)
        crops = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
        text = get_text(crops, lan='kor+eng')
        result.append(text)

    return result

    # for i in range(len(data_area_crops)):
    #     if i == 0:
    #         consignor = get_text_from_img(data_area_crops[0], '화주명')
    #         result.append(consignor)
    #         # print(f'화주명 : {consignor}')
    #         # cv2.imshow('data_area_crops[0]', data_area_crops[0])
    #     if i == 1:
    #         business_number = get_business_num(data_area_crops[1])
    #         result.append(business_number)
    #         # print(f'사업자번호 : {business_number}')
    #         # cv2.imshow('data_area_crops[1]', data_area_crops[1])
    #     if i == 2:
    #         business_name = get_text_from_img(data_area_crops[2],'상호')
    #         result.append(business_name)
    #         # print(f'상호 : {business_name}')
    #         # cv2.imshow('data_area_crops[2]', data_area_crops[2])
    #     if i == 3:
    #         owner_name = get_text_from_img(data_area_crops[3],'대표자명')
    #         result.append(owner_name)
    #         # print(f'대표자명 : {owner_name}')
    #         # cv2.imshow('data_area_crops[3]', data_area_crops[3])
    #     if i == 4:
    #         business_state = get_business_state(data_area_crops[4], 'state')
    #         result.append(business_state)
    #         # print(f'업태 : {business_state}')
    #         # cv2.imshow('data_area_crops[4]', data_area_crops[4])
    #     if i == 5:
    #         business_sector = get_business_state(data_area_crops[5], 'sector')
    #         result.append(business_sector)
    #         # print(f'업종 : {business_sector}')
    #         # cv2.imshow('data_area_crops[5]', data_area_crops[5])
    #     if i == 6:
    #         business_addres = get_multi_line_text_from_img(data_area_crops[6], '사업장주소')
    #         result.append(business_addres)
    #         # print(f'사업장주소 : {business_addres}')
    #         # cv2.imshow('data_area_crops[6]', data_area_crops[6])
    #     if i == 7:
    #         phone_number = get_text_from_img(data_area_crops[7], '전화번호')
    #         result.append(phone_number)
    #         # print(f'전화번호 : {phone_number}')
    #         # cv2.imshow('data_area_crops[7]', data_area_crops[7])
    #     if i == 8:
    #         post_addres = get_multi_line_text_from_img(data_area_crops[8], '우편주소')
    #         result.append(post_addres)
    #         # print(f'우편물주소 : {post_addres}')
    #         # cv2.imshow('data_area_crops[8]', data_area_crops[8])
    #     if i == 9:
    #         e_mail = get_e_mail(data_area_crops[9])
    #         result.append(e_mail)
    #         # print(f'E-Mail : {e_mail}')
    #         # cv2.imshow('data_area_crops[9]', data_area_crops[9])
    # # print(result)
    # return result


def get_business_state(crop, name):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('get_business_state', thr)
    ker = np.ones((3,3), dtype=np.uint8)
    dil = cv2.dilate(thr, ker, iterations=3)
    # cv2.imshow(f'{name}', dil)

    cons = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    texts = []
    psm_config = f'--psm 7'
    i = 0
    for cnt in reversed(cons):
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(thr, (x, y), (x + w, y + h), 255, 2)
        crop = cv2.bitwise_not(thr[y:y+h, x:x+w])
        # cv2.imshow(f'{name}({i})', crop)
        text = pytesseract.image_to_string(crop, lang='kor', config=psm_config)
        text = text.strip('\n')
        texts.append(text)
        # print(f'{name}({i}) = {text}')
        i += 1
    # cv2.imshow('get_business_state', thr)
    # print(texts)
    result = ''.join(texts)
    # print(f'{name} = {result}')
    # result = result.replace('\n','')
    # result = result.strip()

    return result


def get_e_mail(crop):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY)[1]
    psm_config = f'--psm 7'
    result = pytesseract.image_to_string(thr, lang='eng+kor', config=psm_config)
    result = result.strip('\n')
    result = result.strip()

    return result


def get_multi_line_text_from_img(crop, name):
    thr = cv2.threshold(crop, 220, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('get_business_state', thr)
    ker = np.ones((3, 5), dtype=np.uint8)
    dil = cv2.dilate(thr, ker, iterations=3)
    # cv2.imshow(f'get_business_state', dil)

    cons = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    texts = []
    psm_config = f'--psm 7'
    i = 0
    for cnt in reversed(cons):
        x, y, w, h = cv2.boundingRect(cnt)
        # cv2.rectangle(thr, (x, y), (x + w, y + h), 255, 2)
        crop = cv2.bitwise_not(thr[y:y + h, x:x + w])
        # cv2.imshow(f'{name}({i})', crop)
        text = pytesseract.image_to_string(crop, lang='kor', config=psm_config)
        text = text.replace('\n', ' ')
        # print(list(text))
        texts.append(text)
        # print(f'{name}({i}) = {text}')
        i += 1
    # cv2.imshow('get_business_state', thr)
    # print(texts)
    result = ''.join(texts)
    # print(f'{name} = {result}')
    result = result.replace('<', '')
    result = result.replace('>', '')
    # result = result.strip()
    # print(list(result))

    return result
    # thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY)[1]
    # # cv2.imshow('get_multi_line_text_from_img', thr)
    # psm_config = f'--psm 7'
    # result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    # # print(list[result])
    # result = result.replace('\n','')
    # result = result.strip()
    # result = result.replace('ㅅ', 'A')
    # result = result.replace('}', ')')
    # result = result.replace('<', 'C')

    return result


def get_business_num(crop):
    thr = cv2.threshold(crop, 140, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('get_business_num', thr)
    psm_config = f'--psm 7'
    result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    result = result.strip('\n')
    result = result.replace('-','')
    result = list(result)
    result.insert(3, '-')
    result.insert(6, '-')
    result = ''.join(result)

    return result


def get_text_from_img(crop, name):
    thr = cv2.threshold(crop, 200, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow(f'{name}', thr)
    psm_config = f'--psm 7'
    result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    result = result.strip('\n')
    result = result.strip()

    return result

# def get_data_area_crops(data_area_contours, src):
#     # cv2.imshow('get_data_area_crops', src)
#     crops = []
#     i = 0
#     for cnt in reversed(data_area_contours):
#         x, y, w, h = cv2.boundingRect(cnt)
#         crops.append(src[y:y + h, x:x + w])
#         # cv2.imshow(f'get_data_area_crops({i})', crops[i])
#         i += 1
#     return crops


#get_draw_data_area
def get_data_area_contours(del_text_area):
    mask = np.zeros_like(del_text_area)

    thr = cv2mod.get_thr_img(del_text_area, 240, invert=True)
    contours = cv2mod.get_contours(thr, retr='ccomp')

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        mask[y:y + h, x:x + w] = del_text_area[y:y + h, x:x + w]

    mask = cv2mod.get_thr_img(mask, 250)
    mask = cv2mod.get_morph_img(mask, ker=(26, 26), iterations=1)
    result = cv2mod.get_contours(mask)

    return result


#글자 지우는 함수
def get_del_text_area(src):
    del_text_area = src.copy()
    thr = cv2mod.get_thr_img(src, 223, invert=True)  # 223
    dilate = cv2mod.get_dilate_img(thr, ker=(3, 3), iterations=2, dilate=True)
    contours = cv2mod.get_contours(dilate, retr="ccomp")

    for cnt in contours:
        cv2.drawContours(del_text_area, [cnt], 0, (255, 255, 255), cv2.FILLED, cv2.LINE_8)

    return del_text_area


# 전화기 A 마크 지우기
def get_del_phone_and_a(src):
    thr = cv2mod.get_thr_img(src, 250, invert=True)
    contours = cv2mod.get_contours(thr, retr='ccomp')
    i = 0
    for cnt in contours:
        if 2000 < cv2.contourArea(cnt) < 6000:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.9 < w / h < 1.1:
                cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)


#전자세금 계산서 '미발행상태' 출력 함수
def get_text_iti(src):
    result = '발행'
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
            result = get_text(crops_for_text, psm=6)  # , print_text=True)

    return result


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


# file_path = r'C:/Users/realb/PycharmProjects/DailyReport/img/dr/'
# file = 'dr_2022-03-26_150459.png'

# gray = cv2.imread(file_path + file, cv2.IMREAD_GRAYSCALE)
# get_consignor_info(gray)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
