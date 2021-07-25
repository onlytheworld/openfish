# openfish
minecraft 钓鱼脚本

fishing.py 为简易通用版本
    可适用所有机器
    使用传统文本区域检测方法
    使用cnocr识别文本
    使用pyautogui控制屏幕鼠标 
        有一定概率鼠标被屏蔽
        全屏下无法截图
        键盘被屏蔽

fishing-win.py 为windows可用的后台挂机版本，暂为测试脚本
    仅vista版本以后windows系统可用
    修改了文本区域检测算法为mser算法
    使用cnocr识别文本
    修改了屏幕鼠标键盘操作，改用win32api接口，支持后台挂机


计划将要支持：
    mser算法之后的文本框选择方法有待改进
    任意窗口大小检测计算
    反钓鱼脚本检测





