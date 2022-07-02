import cv2
import numpy as np


def get_thr_img(src, thr, invert=False):
    if invert:
        result = cv2.threshold(src, thr, 255, cv2.THRESH_BINARY_INV)[1]
    else:
        result = cv2.threshold(src, thr, 255, cv2.THRESH_BINARY)[1]

    return result


def get_xor_img(src, thr1, thr2, invert=False):
    thr = get_thr_img(src, thr1)
    thr_inv = get_thr_img(src, thr2, invert=True)
    result = cv2.bitwise_xor(thr, thr_inv)
    if invert:
        result = cv2.bitwise_not(result)
    return result


def get_dilate_img(src, ker=(3, 3), iterations=1, dilate=True, invert=False):
    kernel = np.ones(ker, dtype=np.uint8)
    if dilate:
        result = cv2.dilate(src, kernel, iterations=iterations)
    else:
        result = cv2.erode(src, kernel, iterations=iterations)
    if invert:
        result = cv2.bitwise_not(result)

    return result


def get_morph_img(src, ker=(3, 3), morph_open=True, iterations=1, invert=False):
    kernel = np.ones(ker, dtype=np.uint8)
    if morph_open:
        result = (cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel, iterations=iterations))
    else:
        result = (cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel, iterations=iterations))
    if invert:
        result = cv2.bitwise_not(result)

    return result


def get_contours(src, retr="external"):
    if retr == "external":
        result = cv2.findContours(src, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    elif retr == "list":
        result = cv2.findContours(src, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    elif retr == "ccomp":
        result = cv2.findContours(src, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[0]

    return result


def get_crops(src, contours, invert=False, contours_reverse=False, draw_rect=False):
    result = []
    if contours_reverse:
        contours = reversed(contours)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if draw_rect:
            cv2.rectangle(src, (x, y), (x + w, y + h), 255, 3)

        if invert:
            result.append(cv2.bitwise_not(src[y:y + h, x:x + w].copy()))
        else:
            result.append(src[y:y + h, x:x + w].copy())

    return result


def del_area(src, contours):
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(src, (x, y), (x + w, y + h), 255, cv2.FILLED)
    # result = src
    # return result
