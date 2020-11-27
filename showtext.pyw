# AutoRing Project GUI showtext.pyw Not Stable
# 模拟学校上下课铃的程序 GUI部分 不稳定
# Version: release
# Author:lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要库pywin32(GUI) tkinter(GUI)
# 这是个不理想的GUI，包含各种错误和可能的问题。
# 使用shell调用
# 显示第一个参数10s
import sys
import threading
import time
import tkinter

import pywintypes
import win32api
import win32con

arg=sys.argv

text=arg[1]

print(text)

def showmsg(textmsg):
    # 浮动文字
    # Source:https://stackoverflow.com/questions/21840133/how-to-display-text-on-the-screen-without-a-window-using-python
    label = tkinter.Label(text=textmsg, font=('Times New Roman','80'), fg='red', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+0+300")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")
 
    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
 
    def des():
        # 显示时间10s
        time.sleep(10)
        label.destroy()
        label.quit()
 
    ddd=threading.Thread(target=des)
    ddd.start()
 
    label.pack()
    label.mainloop()

showmsg(text)
