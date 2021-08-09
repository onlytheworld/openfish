
from ctypes import byref, sizeof
from ctypes import windll
from ctypes.wintypes import RECT
import time
import win32ui
import win32gui
import win32con
import win32api
from PIL import Image


class mouse:
    def __init__(self, hWnd):
        self.__hWnd = hWnd

    def click(self, x=None, y=None, button='left'):
        if button == 'left':
            VED = win32con.WM_LBUTTONDOWN
            VEU = win32con.WM_LBUTTONUP
        elif button == 'middle':
            VED = win32con.WM_MBUTTONDOWN
            VEU = win32con.WM_MBUTTONUP
        elif button == 'right':
            VED = win32con.WM_RBUTTONDOWN
            VEU = win32con.WM_RBUTTONUP
        win32gui.SendMessage(self.__hWnd, VED)
        time.sleep(0.001)
        win32gui.SendMessage(self.__hWnd, VEU)


class keyboard:
    def __init__(self, hWnd):
        self.__hWnd = hWnd

    def __get_lparam(wparam, isKeyUp=True):
        scanCode = win32api.MapVirtualKey(wparam, 0)
        repeatCount = 1 if isKeyUp else 0
        prevKeyState = 1 if isKeyUp else 0
        transitionState = 1 if isKeyUp else 0
        return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


class screen:
    def __init__(self, hWnd):
        self.__hWnd = hWnd
        self.__CreateDC()

    def __del__(self):
        self.__mfcDC.DeleteDC()
        self.__saveDC.DeleteDC()
        win32gui.DeleteObject(self.__saveBitMap.GetHandle())

    def __CreateDC(self):
        hWndDC = win32gui.GetWindowDC(self.__hWnd)
        self.__mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        self.__saveDC = self.__mfcDC.CreateCompatibleDC()
        self.__saveBitMap = win32ui.CreateBitmap()

    def __bmptrans(self):
        bmpinfo = self.__saveBitMap.GetInfo()
        bmpstr = self.__saveBitMap.GetBitmapBits(True)
        return Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    def CreateBitmap(self,left, top, right, bottom ):
        width = right-left
        height = bottom-top
        self.__saveBitMap.CreateCompatibleBitmap(self.__mfcDC, width, height)
        self.__saveDC.SelectObject(self.__saveBitMap)

    def screenshot(self, left, top, right, bottom):
        width = right-left
        height = bottom-top
        self.__saveDC.BitBlt((0, 0), (width, height),
                             self.__mfcDC, (left, top), win32con.SRCCOPY)
        return self.__bmptrans()

    def SaveBitmapFile(self, name):
        self.__saveBitMap.SaveBitmapFile(self.__saveDC, name)


class window(mouse, keyboard, screen):
    def __init__(self, name):
        self.__hWnd = win32gui.FindWindow(None, name)
        mouse.__init__(self, self.__hWnd)
        keyboard.__init__(self, self.__hWnd)
        screen.__init__(self, self.__hWnd)

    def get_window_size(self):
        try:
            f = windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            print('不支持该获取窗口大小方法')
            f = None
        if f:
            rect = RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(self.__hWnd, DWMWA_EXTENDED_FRAME_BOUNDS, byref(rect), sizeof(rect))
            return rect.right - rect.left, rect.bottom - rect.top


def __print_title(hWnd):
    title = win32gui.GetWindowText(hWnd)
    if title is not '':
        print(title)


def __iswindow(hWnd, hWndList):
    if not hWnd or not win32gui.IsWindow(hWnd) or not win32gui.IsWindowEnabled(hWnd) or not win32gui.IsWindowVisible(hWnd):
        return
    hWndList.append(hWnd)


def display_all_window():
    hWndList = []
    win32gui.EnumWindows(__iswindow, hWndList)
    print('')
    for hWnd in hWndList:
        __print_title(hWnd)
    print('')
