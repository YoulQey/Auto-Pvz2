import pyautogui
import win32gui
import time
pyautogui.PAUSE = 0     # 设置默认暂停时间为0秒
pyautogui.MINIMUM_DURATION = 0      # 设置最小动作持续时间和最小暂停时间为0


import var
from Window import out_text

def click(x, y):
    # back_x, back_y = pyautogui.position()     # 获取鼠标当前位置
    pyautogui.moveTo(x, y)  # 移动到 x, y 的位置
    pyautogui.click()
    # pyautogui.moveTo(back_x, back_y)    # 移动回之前的位置


def get_window(hwnd):
    rect = win32gui.GetClientRect(hwnd)  # 获取窗口的客户区矩形
    ll = list(win32gui.ClientToScreen(hwnd, (rect[0], rect[1] + var.窗口标题高度)))  # 获取窗口左上角的屏幕坐标，并且减去窗口标题高度
    rr = list(win32gui.ClientToScreen(hwnd, (rect[2], rect[3])))  # 获取窗口右下角的屏幕坐标

    if ll[0] < 0 or ll[0] > var.screen_w:   # 防止大于屏幕分辨率报错
        ll[0] = 0

    if ll[1] < 0 or ll[1] > var.screen_h:
        ll[1] = 0

    if rr[0] > var.screen_w or rr[0] <= 0:
        rr[0] = var.screen_w

    if rr[1] > var.screen_h or rr[1] <= 0:
        rr[1] = var.screen_h

    if ll[0] >= rr[0]:          # 有时会出现左上角大于右下角的情况，怪！
        rr[0] = ll[0] + 1

    if ll[1] >= rr[1]:
        rr[1] = ll[1] + 1

    return ll[0], ll[1], rr[0], rr[1]


def 更新窗口与分辨率():

    hwnd = win32gui.GetForegroundWindow()  # 获取当前活动窗口的句柄
    if hwnd:
        var.pixel = get_window(hwnd)
        # print("var.pixel=", var.pixel)
    else:
        out_text("没有找到前台活动窗口，Sleep 1秒")
        time.sleep(1)



