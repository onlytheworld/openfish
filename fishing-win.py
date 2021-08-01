# -*- coding: UTF-8 -*-
import sys
import cv2
import time
import traceback
import numpy as np
from cnocr import CnOcr
if sys.platform == 'win32':
    from selflib import visualmap as vmap
else:
    print('\033[1;31m错误：平台暂不支持\033[0m')


class fisher:
    def __init__(self, name):
        self.__window = vmap.window(name)
        self.__ocr = CnOcr()
        self.__cnt = 0

    def __del__(self):
        print('共钓鱼 %s 次' % self.__cnt)

    def fish(self, buttonshift=52):
        width, height = self.__window.get_window_size()
        print("开始钓鱼：")
        while True:
            try:
                t = time.time()
                fig = self.__window.screenshot(
                    width, height-buttonshift, width*3//4, height*3//5)
                img = np.asarray(fig)
                boxes = self.__mser_detect(img)
                for box in boxes[:3]:
                    x, y, w, h = box
                    if (x+w, y+h) > (width//4-5, height*2//5-5-buttonshift):
                        res = self.__ocr.ocr(img[y:y + h, x:x + w])
                        self.__print(res)
                        if self.__fishsuccess(res):
                            self.__cnt = self.__cnt+1
                            self.__window.click(button='right')
                            time.sleep(0.6)
                            self.__window.click(button='right')
                            print('第 %s 次钓鱼成功' % self.__cnt)
                            time.sleep(2)
                            break
                extime = 0.3-time.time()+t
                time.sleep(extime if extime > 0 else 0)
            except Exception as e:
                print('\033[1;31m错误：异常退出\033[0m')
                traceback.print_exc()
                break
            except KeyboardInterrupt:
                print('正常退出')
                break

    def screencheck(self, buttonshift=52):
        width, height = self.__window.get_window_size()
        fig = self.__window.screenshot(
            width, height-buttonshift, width*3//4, height*3//5)
        img = np.asarray(fig)
        boxes = self.__mser_detect(img)
        cv2.imshow("range.png", img)
        cv2.waitKey(0)
        return input('\033[1;33m区域校准是否成功:\n\t1、成功，开始钓鱼\n\t2、重新校准\n\t3、放弃\n输入：\033[0m')

    def __fishsuccess(self, res):
        for r in res:
            if (('浮' in r or '漂' in r or '溧' in r or ('钓' in r and '钩' in r and '鱼' in r)) and ('溅' in r or '贱' in r or '起' in r or '水' in r or '丞' in r or '花' in r)):
                return True

    def __mser_detect(self, img, flag=False):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create(_min_area=1000)
        _, boxes = mser.detectRegions(gray)
        if flag:
            plotimg = img.copy()
            for box in boxes:
                x, y, w, h = box
                if (x+w, y+h) > (861-700-5, 468-300-5):
                    cv2.rectangle(plotimg, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('1', plotimg)
            cv2.waitKey(0)
        return boxes

    def __print(self, res):
        print('识别汉字：', end='')
        for r in res:
            print('%s' % ''.join(r), ' ', end='')
        print('')


if __name__ == '__main__':
    userin = input(
        '\033[1;33m请输入需要的操作序号：\n\t1、打印所有窗口名字\n\t2、钓鱼\n\t3、校准\n\t4、退出\n输入：\033[0m')
    PRINT_FLAG = '1'
    FISH_FLAG = '2'
    ALIGN_FLAG = '3'
    EXIT_FLAG = '4'
    while userin != EXIT_FLAG:
        if userin == PRINT_FLAG:
            vmap.display_all_window()
        elif userin == ALIGN_FLAG:
            name = input('\033[1;33m请输入 minecraft 对应窗口名：\033[0m')
            fi = fisher(name)
            SUCCESS_FLAG = '1'
            CONTINUE_FLAG = '2'
            QUIT_FLAG = '3'
            flag = fi.screencheck()
            shif = 52
            while flag == CONTINUE_FLAG:
                shif = int(input('\033[1;33m请输入校准值（默认52）\033[0m'))
                flag = fi.screencheck(shif)
            if flag == SUCCESS_FLAG:
                fi.fish(shif)
            break
        elif userin == FISH_FLAG:
            name = input('\033[1;33m请输入 minecraft 对应窗口名：\033[0m')
            fisher(name).fish()
            break
        userin = input(
            '\033[1;33m请输入需要的操作序号：\n\t1、打印所有窗口名字\n\t2、钓鱼\n\t3、校准\n\t4、退出\n输入：\033[0m')
    input('按回车键结束程序')

