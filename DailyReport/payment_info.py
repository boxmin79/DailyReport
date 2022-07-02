import cv2
import numpy as np
import pytesseract
import cv2mod

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract'


def get_payment_info(src):
    result = []

    text_iti = get_text_iti(src)
    # print(text_iti)

    get_del_icon(src)

    del_text_area = get_del_text_area(src)
    # cv2.imshow('del_text_area', del_text_area)

    data_area_contours = get_data_area_contours(del_text_area)
    # print(len(data_area_contours))

    crops_for_texts = cv2mod.get_crops(src, data_area_contours, invert=False, contours_reverse=True)

    i = 0
    # for crops_for_text in crops_for_texts:
    for crops_for_text in crops_for_texts[1:6]:
    #     cv2.imshow(f'{i}', crops_for_text)
        thr = cv2mod.get_thr_img(crops_for_text, 200, invert=True)
        dilate = cv2mod.get_dilate_img(thr, ker=(15, 15), iterations=1)
        contours = cv2mod.get_contours(dilate)
        crops = cv2mod.get_crops(thr, contours, invert=True, contours_reverse=True)
        text = get_text(crops, lan='kor+eng')
        if '원' in text:
            result.append(int(text.replace('원', '').replace(',', '')))
        else:
            result.append(text)
        i += 1
    # print(result)

    result[4] = result[4][1:-1]
    result = result[:5]
    result.insert(len(result) - 1, text_iti)

    if result[2] == '선/착불':
        result[4] = '수기발행'
        result.insert(len(result) - 1, '수기')
    elif text_iti == '전자발행' and result[2] == '인수증':
        result.insert(len(result) - 1, '전자')
    else:
        result.insert(len(result) - 1, '우편')

    return result


def get_collect_state(crop):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY_INV)[1]
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


def get_e_mail(crop):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY)[1]
    psm_config = f'--psm 7'
    result = pytesseract.image_to_string(thr, lang='eng+kor', config=psm_config)
    result = result.strip('\n')
    result = result.strip()

    return result


def get_multi_line_text_from_img(crop):
    thr = cv2.threshold(crop, 240, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('get_multi_line_text_from_img', thr)
    psm_config = f'--psm 6'
    result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    # print(list[result])
    result = result.replace('\n', '')
    result = result.strip()
    result = result.replace('ㅅ', 'A')
    result = result.replace('}', ')')
    result = result.replace('<', 'C')

    return result


def get_business_num(crop):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY)[1]
    psm_config = f'--psm 11'
    result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    result = result.strip('\n')
    result = result.replace('-', '')
    result = list(result)
    result.insert(3, '-')
    result.insert(6, '-')
    result = ''.join(result)

    return result


def get_text_from_img(crop):
    thr = cv2.threshold(crop, 160, 255, cv2.THRESH_BINARY)[1]
    psm_config = f'--psm 7'
    result = pytesseract.image_to_string(thr, lang='kor', config=psm_config)
    result = result.strip('\n')
    result = result.strip()

    return result


# get_draw_data_area
def get_data_area_contours(del_text_area):
    mask = np.zeros_like(del_text_area)

    thr = cv2mod.get_thr_img(del_text_area, 240, invert=True)
    # cv2.imshow('get_data_area_contours', thr)
    contours = cv2mod.get_contours(thr, retr='ccomp')

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        mask[y:y + h, x:x + w] = del_text_area[y:y + h, x:x + w]

    mask = cv2mod.get_thr_img(mask, 250)
    mask = cv2mod.get_morph_img(mask, ker=(28, 28), iterations=1)
    # cv2.imshow('get_data_area_contours', mask)
    result = cv2mod.get_contours(mask)

    return result


def get_del_icon(src):
    thr = cv2mod.get_thr_img(src, 250, invert=True)
    contours = cv2mod.get_contours(thr, retr='ccomp')

    for cnt in contours:
        if 6000 < cv2.contourArea(cnt) < 10000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)


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
    result = '전자발행'
    thr_xor = cv2mod.get_xor_img(src, 220, 230)
    morph = cv2mod.get_morph_img(thr_xor, ker=(3, 3), morph_open=False, iterations=2, invert=True)
    contours = cv2mod.get_contours(morph)

    if len(contours) > 0:
        crops = cv2mod.get_crops(src, contours)
        cv2mod.del_area(src, contours)
        xor_crop_for_text = cv2mod.get_xor_img(crops[0], 100, 160, invert=True)
        morph_for_text = cv2mod.get_morph_img(xor_crop_for_text)
        contours_for_text = cv2mod.get_contours(morph_for_text, retr="external")

        if len(contours_for_text) > 0:
            crops_for_text = cv2mod.get_crops(xor_crop_for_text, contours_for_text)
            result = get_text([crops_for_text[0]])  # , print_text=True)
            if '_' in result:
                result = result.replace('_', '')

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
# file = 'dr_2022-03-26_150500.png'
#
# gray = cv2.imread(file_path + file, cv2.IMREAD_GRAYSCALE)
# get_payment_info(gray)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
