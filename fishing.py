# -*- coding: UTF-8 -*-
import pyautogui
import time
from cnocr import CnOcr
import cv2
import numpy as np
import sys

pyautogui.PAUSE = 1

def findfish(res):
    for line in res:
        if(line == ['浮', '漂', ':', '溅', '起', '水', '花']):
            return True
    return False

def fish():
    ocr = CnOcr()
    if(1):
        t=time.time()
        # 1、截图，手动定位字幕大致区域
        if(len(sys.argv) == 5):
            fig = pyautogui.screenshot(region=(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
        else:
            fig = pyautogui.screenshot(region=(1775, 700, 130, 300))
        # 2、检测文本所在区域
        img = np.asarray(fig)
        textImg = detect(img)
        # 3、利用cnocr识别文本
        res = ocr.ocr(textImg)
        print("Predicted Chars:", res)
        print(time.time()-t)
        # 4、通过文本判断是否收杆
        if(findfish(res)):
            pyautogui.click(button='right')
            pyautogui.click(button='right')
            time.sleep(1)
        else:
            time.sleep(0.5)  

def detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilation = preprocess(gray)
    x, y, w, h = findTextRegion(dilation)
    return img[y:y + h, x:x + w]

def preprocess(gray):
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
    _, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
    dilation = cv2.dilate(binary, element2, iterations=1)
    erosion = cv2.erode(dilation, element1, iterations=1)
    dilation2 = cv2.dilate(erosion, element2, iterations=2)
    return dilation2

def findTextRegion(img):
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = 0
    maxContour = 0
    if(len(contours)==0):
        return 0,0,0,0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > maxArea:
            maxArea = area
            maxContour = cnt
    x, y, w, h = cv2.boundingRect(maxContour)
    return x, y, w, h

if __name__ =='__main__':
    fish()
