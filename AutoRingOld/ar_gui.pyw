# AutoRing.pyw GUI ar_gui.pyw Not Stable
# 模拟学校上下课铃的程序 GUI部分 不稳定
# Version: developer beta
# Author:lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要库pywin32(GUI) tkinter(GUI)
# 这是个不理想的GUI，包含各种错误和可能的问题。
import tkinter
import threading
import time
import win32api, win32con, pywintypes
import datetime
 
stcuti=datetime.datetime.now()
strstcuti=str(stcuti.year)+"-"+str(stcuti.month)+"-"+str(stcuti.day)+"-"+str(stcuti.hour)+"-"+str(stcuti.minute)+"-"+str(stcuti.second)
logname="AutoRingGUILog-"+strstcuti+".txt"
 
def logit(msg):
    # 日志函数
    print(str(msg))
    with open(logname,"a") as logfile:
        content="["+str(datetime.datetime.now())+"]"+str(msg)+"\n"
        logfile.write(content)
 
def showmsg(textmsg):
    # 浮动文字
    logit("[GUI]Start"+" msg:"+str(textmsg))
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
        # 显示时间
        time.sleep(30)
        label.destroy()
        label.quit()
 
    ddd=threading.Thread(target=des)
    ddd.start()
 
    label.pack()
    label.mainloop()
 
    logit("[GUI]Exit"+" msg:"+str(textmsg))
 
def clearmsg():
    # Clear浮动文字，就是上个函数重写了一遍
    logit("[GUI]Clear")
    # Source:https://stackoverflow.com/questions/21840133/how-to-display-text-on-the-screen-without-a-window-using-python
    label = tkinter.Label(text="", font=('Times New Roman','10'), fg='black', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry("+0+0")
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
        # 显示时间
        time.sleep(5)
        label.destroy()
        label.quit()
 
    ddd=threading.Thread(target=des)
    ddd.start()
 
    label.pack()
    label.mainloop()
 
    logit("[GUI]Clear Exit")
 
logit("!!!!!!本次日志开始!!!!!!")
logit("GUI日志文件"+logname)
 
def sleepto(hour,minute):
    # Sleep到某时
    nowtime=datetime.datetime.now()
    nowmon=nowtime.month
    nowday=nowtime.day
    nowye=nowtime.year
 
    strthe=str(nowye)+"-"+str(nowmon)+"-"+str(nowday)+" "+str(hour)+":"+str(minute)+":"+"0.0"
    thetime=datetime.datetime.strptime(strthe,"%Y-%m-%d %H:%M:%S.%f")
    delta=(thetime-nowtime).seconds
    time.sleep(delta)
 
def ringat(hour,minute,msg):
    # 在某时提醒，超过3h不提醒
    logit("[RingAt]"+str(hour)+" "+str(minute)+" "+str(msg))
    passit=0
    nowtime=datetime.datetime.now()
    nowmon=nowtime.month
    nowday=nowtime.day
    nowye=nowtime.year
 
    strthe=str(nowye)+"-"+str(nowmon)+"-"+str(nowday)+" "+str(hour)+":"+str(minute)+":"+"0.0"
    thetime=datetime.datetime.strptime(strthe,"%Y-%m-%d %H:%M:%S.%f")
    delta=(thetime-nowtime).seconds
    logit("[RingAt]"+"Delta:"+str(delta))
    if delta>=10800:
        passit=1
        logit("[RingAt]Pass")
    if passit==0:
        logit("[RingAt]Sleeping...")
        time.sleep(delta)
        showmsg(str(msg))
        clearmsg()
        # 用空白刷新屏幕浮动字符
        # 不是个好办法但目前只能如此
 
ringat(8,0,"1:Class Begin")
ringat(8,40,"1:Class Over")
ringat(8,50,"2:Class Begin")
ringat(9,30,"2:Class Over")
ringat(9,40,"3:Class Begin")
ringat(10,20,"3:Class Over")
ringat(10,50,"4:Class Begin")
ringat(11,30,"4:Class Over")
ringat(11,40,"5:Class Begin")
ringat(12,20,"5:Class Over")
ringat(13,50,"6:Class Begin")
ringat(14,30,"6:Class Over")
ringat(14,40,"7:Class Begin")
ringat(15,20,"7:Class Over")
ringat(15,50,"8:Class Begin")
ringat(16,30,"8:Class Over")
ringat(16,40,"9:Class Begin")
ringat(17,20,"9:Class Over")
ringat(17,50,"1st Self-study Begin")
ringat(18,50,"1st Self-study Over")
ringat(19,0,"2nd Self-study Begin")
ringat(20,0,"2nd Self-study Over")
ringat(20,10,"3rd Self-study Begin")
ringat(22,0,"3rd Self-study Over")
 
logit("Work done.Program Exit.")
