#!/usr/bin/env python3
# AutoRing Project Main App autoring.pyw
# AutoRing项目主程序
# Version: stable-1-Non-LTS-BugFix-Final
# Author: lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要第三方库pygame(Sound) 可能需要pywin32 tkinter(GUI) 外部二进制程序cmdmp3 ffmpeg
# 部分功能为Windows设计，可能无法跨平台运行或需要修改。
import datetime
import json
import logging
import os
import random
import subprocess
import sys
import threading
import time

import pygame

# 初始化Pygame Mixer
pygame.mixer.init(buffer=10240)
# Bigger buffer to avoid strange sound effect when high I/O occurs.

# 配置logging
# 设置日志文件名、记录等级和格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(origin)s] %(message)s"
logging.basicConfig(filename='autoring.log',
                    level=logging.DEBUG, format=LOG_FORMAT)


def infoLog(origin="UNKNOWN", msg="UNKNOWN"):
    # Info日志函数
    logging.info(str(msg), extra={'origin': str(origin)})
    print(str(origin)+":"+str(msg))  # 打印日志内容


def playSound(filename="begin.mp3"):
    # 播放音乐filename
    # 也可以选用pygame.mixer的其他函数
    file = str(filename)
    try:
        pygame.mixer.music.load(file)
        infoLog("playSound", "Play "+file+" .")
        pygame.mixer.music.play()
    except:
        infoLog("playSound", "pygame.error!")  # 糟糕的错误处理，需要改进。
        altPlaySound(file)


def getSeconds(hour, minute, second=0):
    # 获取到某时刻秒
    nowtime = datetime.datetime.now()
    nowmon = nowtime.month
    nowday = nowtime.day
    nowye = nowtime.year
    strthe = str(nowye)+"-"+str(nowmon)+"-"+str(nowday) + \
        " "+str(hour)+":"+str(minute)+":"+str(second)+".0"
    thetime = datetime.datetime.strptime(strthe, "%Y-%m-%d %H:%M:%S.%f")
    delta = (thetime-nowtime).seconds
    return delta


def sleepTo(hour, minute, second=0):
    # 等待到某时 Sleep to sometime
    delay = 0
    #####################################################
    # Delay to sync with the stupid school timing system.
    delay = -60
    infoLog("sleepTo", "delay="+str(delay)+" .")
    #####################################################
    infoLog("sleepTo", str(hour)+" "+str(minute)+" "+str(second))
    delta = getSeconds(int(hour), int(minute), int(second))+delay
    if delay < 0:
        # delay<0时可能出现delta<0导致错误
        infoLog("sleepTo", "Chk delta "+str(delta)+".")
        if delta < 0:
            delta = 1
            infoLog("sleepTo", "Delta<0,reset.")
    infoLog("sleepTo", "Delta:"+str(delta)+" Sleeping...")
    time.sleep(delta)


def getPass(hour, minute, second=0):
    # Get if pass
    # return 1 when pass
    # 获取是否已过当前时间
    nowtime = datetime.datetime.now()
    ifpass = 0
    if int(hour) < nowtime.hour:
        ifpass = 1
    if int(hour) == nowtime.hour:
        if int(minute) < nowtime.minute:
            ifpass = 1
    if int(hour) == nowtime.hour:
        if int(minute) == nowtime.minute:
            if int(second) < nowtime.second:
                ifpass = 1
    return ifpass


def getWeekday(date=datetime.datetime.now()):
    # 获取星期1-7
    day = date.weekday()
    intday = int(day)+1
    ###################
    # Force Monday
    # intday = 1
    # End Force Monday
    ###################
    # Force Normal
    # intday = 2
    # End Force Normal
    ###################
    return intday


def getFilename(stat=6):
    # 根据事件获取文件名
    intstat = int(stat)
    fn = "alarm.mp3"  # Failsafe
    if intstat == 1:
        # normal上课
        # fn = "begin.mp3"
        fn = "nosound.mp3"
    if intstat == 2:
        # normal下课
        # fn = "over.mp3"
        fn = "nosound.mp3"
    if intstat == 3:
        # 放学 在此保留Failsafe
        # 需要注意放学事件的实际解决方案不同，见ringAt函数和randPlaySound函数。
        # fn = "afterschool.mp3"
        fn = "nosound.mp3"
    if intstat == 4:
        # special上课
        fn = "begin.mp3"
    if intstat == 5:
        # special下课
        fn = "over.mp3"
    if intstat == 6:
        # No sound 无声
        fn = "nosound.mp3"
    return fn


def randPlaySound():
    # Random Music Player
    # 1.mp3 2.mp3 3.mp3 4.mp3 etc.
    # 随机播放音频
    # 文件名1.mp3 2.mp3 ...... 17.mp3 ...... 30.mp3
    randnum = random.randint(1, 30)  # 生成文件名中的随机数部分
    #####################################
    # randnum = 17  # Force 17 强制“随机”
    #####################################
    randstr = str(randnum)
    fnstr = randstr+".mp3"
    infoLog("randPlaySound", fnstr)
    try:
        infoLog("json", "Try to read json.")  # 与autoconvert.py配合使用
        with open("music.json", "r") as data:
            filen = json.load(data)
        infoLog("json", str(filen))
        infoLog("chkfile", "Checking file.")
        with open(filen, "r") as testfile:  # 检测文件存在性
            infoLog("chkfile", "File exists.")
        playSound(filen)
        with open("music.json", "w") as data:  # 覆写json使其失效
            data.write("init")
            infoLog("json", "Rewrite json.")
    except:
        infoLog("json", "Failed.")  # 若出错
        playSound(fnstr)


def showMsgMain(msg):
    # Call showtext
    # Add pythonw to your $PATH
    # 调用showtext.pyw
    # pythonw需要被加入环境变量PATH
    infoLog("showMsgMain", str(msg))
    subprocess.call(["pythonw", "showtext.pyw", str(msg)])
    infoLog("showMsgMain", "Exit.")


def showMsg(msg):
    # Threading to avoid waiting.
    # 多线程用于避免等待
    infoLog("showMsg", str(msg))
    ddd = threading.Thread(target=showMsgMain, args=[str(msg)])
    ddd.start()


def altPlaySoundMain(file):
    # Call cmdmp3 to play sound.
    # In case of pygame.error
    # 调用cmdmp3.exe
    # 避免随机（？）出现的pygame.error影响播放
    infoLog("altPlaySoundMain", str(file))
    subprocess.call(["cmdmp3", str(file)])
    infoLog("altPlaySoundMain", "Exit.")


def altPlaySound(file):
    # Threading to avoid waiting.
    # 多线程
    infoLog("altPlaySound", str(file))
    ddd = threading.Thread(target=altPlaySoundMain, args=[str(file)])
    ddd.start()


def ringAt(hour, minute, second=0, stat=1, info="UNKNOWN"):
    # 响铃函数
    # stat 1 常规上课 2 常规下课 3 放学 4 特殊上课 5 特殊下课 6 无声
    # 调用举例ringAt(12,12,14,2,"Test") 12:12:14 常规下课 日志信息和屏幕显示"Test"
    # 可以用多线程和循环代替当前方案，但不具有必要性。
    infoLog("ringAt", str(hour)+":"+str(minute)+":" +
            str(second)+" "+str(stat)+" "+str(info))
    if getPass(int(hour), int(minute), int(second)) == 1:
        infoLog("ringAt", "Pass!")
    else:
        infoLog("ringAt", "Sleeping...")
        sleepTo(int(hour), int(minute), int(second))
        filename = getFilename(stat)
        stat = int(stat)
        if stat != 3:
            playSound(filename)
        if stat == 3:
            randPlaySound()
        # 屏幕显示
        # showMsg(str(info))


def pyExecAt(hour, minute, second=0, code="print('No code.')"):
    # 在某时执行Python代码
    # 使用exec()
    # 调用举例pyExecAt(小时，分钟，秒，Python代码)
    infoLog("pyExecAt", str(hour)+":"+str(minute)+":" +
            str(second)+" "+str(code))
    if getPass(int(hour), int(minute), int(second)) == 1:
        infoLog("pyExecAt", "Pass!")
    else:
        infoLog("pyExecAt", "Sleeping...")
        sleepTo(int(hour), int(minute), int(second))
        infoLog("pyExecAt", "Exec.")
        exec(str(code))


def shutitdown():
    # 关机操作
    infoLog("shutitdown", "Shutdown.")
    # os.system("shutdown -s -t 600")  # 10分钟定时关机
    infoLog("shutitdown", "Wait.")
    time.sleep(10)  # 等待执行和GUI提示
    infoLog("shutitdown", "LockWorkStation")
    os.system("rundll32.exe user32.dll,LockWorkStation")  # 锁定工作站
    infoLog("shutitdown", "Wait.")
    time.sleep(540)  # 等待音乐播放完成退出程序 9分钟
    infoLog("shutitdown", "Turn off the monitor.")
    # 关闭显示器
    os.system(
        "powershell (Add-Type '[DllImport(\"user32.dll\")]^public static extern int PostMessage(int hWnd, int hMsg, int wParam, int lParam);' -Name a -Pas)::PostMessage(-1,0x0112,0xF170,2)")
    infoLog("shutitdown", "Exit.")
    sys.exit()

#######################################################


def showTextScript(usermsg="No arg."):
    # 整合版本被设计用于紧急用途，但也可以在生产环境使用。
    # AutoRing Project GUI Not Stable
    # AutoRing项目 GUI部分 不稳定
    # Version: release
    # Author: lwd-temp
    # https://github.com/lwd-temp/AutoRing.py
    # 需要库pywin32(GUI) tkinter(GUI)
    # 这是个不理想的GUI，包含各种错误和可能的问题。
    # 使用shell调用
    # 显示第一个参数10s
    # import sys
    # import threading
    # import time
    import tkinter

    import pywintypes
    import win32api
    import win32con

    arg = sys.argv
    try:
        text = arg[2]  # It's [2] here.
    except:
        try:
            text = usermsg
        except:
            text = "Arg Error"

    infoLog("showTextScript", text)

    # print(text)

    def showmsg(textmsg):
        # 浮动文字
        # Source: https://stackoverflow.com/questions/21840133/how-to-display-text-on-the-screen-without-a-window-using-python
        label = tkinter.Label(text=textmsg, font=(
            'Times New Roman', '80'), fg='red', bg='white')
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

        ddd = threading.Thread(target=des)
        ddd.start()

        label.pack()
        label.mainloop()

    showmsg(text)
    sys.exit()
#######################################################
#######################################################


def autoConvertScript():
    # 整合版本被设计用于紧急用途，但也可以在生产环境使用。
    # AutoRing项目 自助式自动化放学铃设置 面向用户
    # import datetime
    # import json
    # import logging
    # import subprocess
    # import sys

    # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # logging.basicConfig(filename='ac.log',
    #                     level=logging.DEBUG, format=LOG_FORMAT)

    nowtime = datetime.datetime.now()
    filename = str(nowtime.year)+"-"+str(nowtime.month)+"-"+str(nowtime.day) + \
        "-"+str(nowtime.hour)+"-"+str(nowtime.minute) + \
        "-"+str(nowtime.second)+".mp3"
    infoLog("autoConvertScript", "Run.")

    def generate_random_str(randomlength=16):
        # 生成一个指定长度的随机字符串
        # Source: https://www.jb51.net/article/173670.htm
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def ffmpeg(infi, outfi):
        # Call ffmpeg
        infoLog("autoConvertScript", "ffmpeg "+str(infi)+" "+str(outfi))
        subprocess.call(["ffmpeg", "-i", str(infi), str(outfi)])
        infoLog("autoConvertScript", "ffmpeg exit.")

    print("自助式自动化放学铃设置 Beta2版本")
    print("您的所有操作都将被记录备案，请不要恶意提交。")
    # print("不一定需要重命名媒体文件为123并将其复制到桌面。")

    try:
        infoLog("autoConvertScript", "Try to read json.")
        with open("music.json", "r") as data:
            filen = json.load(data)
        infoLog("autoConvertScript", "Json exists.")
        with open(filen, "r") as testfile:
            infoLog("autoConvertScript", "File exists.")
        print("已存在人工设置。")
        infoLog("autoConvertScript", "Operation exists.")
        oped = 1
    except:
        infoLog("autoConvertScript", "Operation chk OK.")
        print("当前无人工设置。")
        oped = 0

    # To disable functions.
    #########################
    # oped = 1
    #########################

    if oped == 1:
        print("当日已存在人工设置，为确保不覆写设置已禁止操作。")
        print("按Enter退出程序。")
        userinput = input()
        infoLog("autoConvertScript", str(userinput))
        if userinput != "debug":
            sys.exit()
        else:
            print("Input Debugger Key:")
            dkr = str(nowtime.year+2)+str(nowtime.month*2) + \
                str(nowtime.day+2)  # Debugger Key生成
            dk = input()
            infoLog("autoConvertScript", str(dk))
            if dk == dkr:
                infoLog("autoConvertScript", "Hello,debugger!")
                with open("music.json", "w") as data:
                    data.write("init")
                    infoLog("autoConvertScript", "Json rewrite done.")
                    print("Json已覆写。")
            else:
                infoLog("autoConvertScript", "Wrong Debugger Key.")
                sys.exit()

    fp = input("输入媒体文件路径或直接将文件拖入窗口并按下Enter：")
    while fp.rstrip() == "":
        infoLog("autoConvertScript", "Empty file path.")
        fp = input("输入媒体文件路径或直接将文件拖入窗口并按下Enter：")

    infoLog("autoConvertScript", "用户输入："+fp+" 。")

    print("用户输入："+fp+" 。")

    # 特殊验证词汇
    forbidden_words = ["周杰伦", "摇滚", "流行", "榜", "测试词汇", "热门"]

    for word in forbidden_words:
        if str(word) in fp:
            infoLog("autoConvertScript", "Forbidden word in fp:"+str(word))
            print("检测到可能的非法提交，请输入下方验证码。")
            randstr = str(generate_random_str(5))
            infoLog("autoConvertScript", randstr)
            print("验证码："+randstr)
            userinstr = input("请输入验证码：")
            infoLog("autoConvertScript", userinstr)
            if userinstr == randstr:
                infoLog("autoConvertScript", "User Check Pass.")
                print("验证通过。")
            else:
                infoLog("autoConvertScript", "User Check Failed.")
                print("验证失败。")
                sys.exit()

    # Fix cmd file dragging path complete feature
    if fp[0] == '"':
        if fp[-1] == '"':
            fp = fp[1:-1]

    infoLog("autoConvertScript", "文件路径："+fp+" 。")

    print("文件路径："+fp+" 。")

    comment = input("输入本次提交描述并按Enter：")
    infoLog("autoConvertScript", "Comment:"+comment+" .")

    try:
        with open(fp, "r") as testfile:
            print("文件存在。")
            infoLog("autoConvertScript", "File exists.")
    except:
        print("文件不存在或权限不足。")
        infoLog("autoConvertScript", "File failed.")
        sys.exit()

    print("调用ffmpeg，请注意错误信息...")
    ffmpeg(fp, filename)
    print("转码结束，请注意错误信息。")

    try:
        with open(filename, "r") as testfile:
            infoLog("autoConvertScript", "File ok.")
    except:
        infoLog("autoConvertScript", "File failed.")
        print("文件未生成，转码错误。")
        sys.exit()

    print("写入json。")
    infoLog("autoConvertScript", "Try to write json.")
    with open("music.json", "w") as data:
        json.dump(filename, data)

    infoLog("autoConvertScript", "Done")
    print("完成，你可以安全地关闭窗口了。")
    infoLog("autoConvertScript", "Exit.")

    sys.exit()
#######################################################


def console():
    # Console Mode
    infoLog("console", "Welcome to the AR Console!")
    infoLog("console", "Hello from the AR Developer!")
    infoLog("HELP", "ringAt(hour,minute,second,stat,info)")
    infoLog("HELP", "stat:1-normBegin 2-normOver 3-AfterSchool 4-specBegin 5-specOver 6-NoSound")
    infoLog("HELP", "infoLog(origin,msg)")
    infoLog("HELP", "getSeconds(hour,minute,second)")
    infoLog("HELP", "playSound(filename)")
    infoLog("HELP", "pyExecAt(hour,minute,second,code)")
    infoLog("HELP", "showMsg(msg)")
    infoLog("HELP", "More functions available.Please read the source code.")
    infoLog("console", "Syntax: FUNCTION [ARG1] [ARG2] ...")
    infoLog("console", "Example: ringAt 12 33 23 3 hello")
    infoLog("console", "DANGEROUS!The AR Console is designed for developers.")
    infoLog("console", "Please read the full source code before using the console.")
    while True:
        userinput = input("ARConsole>>>")
        while userinput.rstrip() == "":
            infoLog("console", "Empty.")
            userinput = input("ARConsole>>>")
        userinput = userinput.split()
        infoLog("console", str(userinput))
        if userinput[0] == "exit":
            infoLog("console", "Exit.")
            sys.exit()
        else:
            userfunc = userinput[0]
            infoLog("console", userfunc)
            try:
                userarg = userinput[1:]
                infoLog("console", str(userarg))
            except:
                userarg = []
                infoLog("console", "Arg Error, use empty arg.")
        try:
            infoLog("console", "run")
            execthread = "threading.Thread(target=" + \
                str(userfunc)+", args="+str(userarg)+").start()"
            infoLog("console", execthread)
            exec(execthread)
        except:
            infoLog("console", "ERROR!")


def zwt():
    # 此彩蛋即将结束支持
    # In memory of the one who made a difference to me.
    # import datetime
    date = datetime.datetime.today()
    if date.month == 4:
        if date.day >= 20:
            infoLog("zwt", "Happy birthday ZWT!")
    if date.month == 5:
        if date.day == 5:
            count = 0
            while count != 4:
                infoLog("zwt", "Happy birthday ZWT!")
                count = count+1
        if date.day <= 15:
            infoLog("zwt", "Happy birthday ZWT!")


def dailySchedule():
    # 标准时间表
    infoLog("dailySchedule", "Hello from the AR Developer!")
    if getWeekday() == 1:
        # 若周一
        infoLog("dailySchedule", "Today is Monday.")
        ringAt(7, 40, 0, 1, "1:Class Begin")
        ringAt(8, 20, 0, 2, "1:Class Over")
        ringAt(8, 30, 0, 1, "2:Class Begin")
        ringAt(9, 10, 0, 2, "2:Class Over")
        ringAt(9, 20, 0, 1, "3:Class Begin")
        ringAt(10, 0, 0, 2, "3:Class Over")
        ringAt(10, 30, 0, 1, "4:Class Begin")
        ringAt(11, 10, 0, 2, "4:Class Over")
        ringAt(11, 20, 0, 1, "5:Class Begin")
        ringAt(12, 0, 0, 2, "5:Class Over")
        ringAt(13, 40, 0, 1, "6:Class Begin")
        ringAt(14, 20, 0, 2, "6:Class Over")
        ringAt(14, 30, 0, 1, "7:Class Begin")
        ringAt(15, 10, 0, 2, "7:Class Over")
        ringAt(15, 40, 0, 1, "8:Class Begin")
        ringAt(17, 0, 0, 2, "9:Class Over")
        ringAt(17, 40, 0, 1, "1st Self-study Begin")
        ringAt(18, 40, 0, 2, "1st Self-study Over")
        ringAt(18, 50, 0, 1, "2nd Self-study Begin")
        ringAt(19, 50, 0, 2, "2nd Self-study Over")
        ringAt(20, 0, 0, 4, "3rd Self-study Begin")
        ringAt(22, 0, 0, 3, "3rd Self-study Over")
        pyExecAt(22, 0, 30, "shutitdown()")
    elif getWeekday() == 7:
        # 若周日
        infoLog("dailySchedule", "Today is Sunday.")
        ringAt(12, 0, 0, 3, "School Over")
        pyExecAt(12, 0, 30, "shutitdown()")
    elif getWeekday() == 6:
        # 若周六
        infoLog("dailySchedule", "Today is Saturday.")
        ringAt(8, 0, 0, 1, "1:Class Begin")
        ringAt(8, 40, 0, 2, "1:Class Over")
        ringAt(8, 50, 0, 1, "2:Class Begin")
        ringAt(9, 30, 0, 2, "2:Class Over")
        ringAt(9, 40, 0, 1, "3:Class Begin")
        ringAt(10, 20, 0, 2, "3:Class Over")
        ringAt(10, 30, 0, 1, "4:Class Begin")
        ringAt(11, 10, 0, 2, "4:Class Over")
        ringAt(11, 20, 0, 1, "5:Class Begin")
        ringAt(12, 0, 0, 2, "5:Class Over")
        ringAt(13, 40, 0, 1, "6:Class Begin")
        ringAt(14, 20, 0, 2, "6:Class Over")
        ringAt(14, 30, 0, 1, "7:Class Begin")
        ringAt(15, 10, 0, 2, "7:Class Over")
        ringAt(15, 40, 0, 1, "8:Class Begin")
        ringAt(17, 0, 0, 2, "9:Class Over")
        ringAt(17, 40, 0, 1, "1st Self-study Begin")
        ringAt(18, 40, 0, 2, "1st Self-study Over")
        ringAt(18, 50, 0, 1, "2nd Self-study Begin")
        ringAt(19, 50, 0, 2, "2nd Self-study Over")
        ringAt(20, 0, 0, 4, "3rd Self-study Begin")
        ringAt(22, 0, 0, 3, "3rd Self-study Over")
        pyExecAt(22, 0, 30, "shutitdown()")
    else:
        infoLog("dailySchedule", "Today is Normal.")
        ringAt(7, 40, 0, 1, "1:Class Begin")
        ringAt(8, 20, 0, 2, "1:Class Over")
        ringAt(8, 30, 0, 1, "2:Class Begin")
        ringAt(9, 10, 0, 2, "2:Class Over")
        ringAt(9, 20, 0, 1, "3:Class Begin")
        ringAt(10, 0, 0, 2, "3:Class Over")
        ringAt(10, 30, 0, 1, "4:Class Begin")
        ringAt(11, 10, 0, 2, "4:Class Over")
        ringAt(11, 20, 0, 1, "5:Class Begin")
        ringAt(12, 0, 0, 2, "5:Class Over")
        ringAt(13, 40, 0, 1, "6:Class Begin")
        ringAt(14, 20, 0, 2, "6:Class Over")
        ringAt(14, 30, 0, 1, "7:Class Begin")
        ringAt(15, 10, 0, 2, "7:Class Over")
        ringAt(15, 40, 0, 1, "8:Class Begin")
        ringAt(17, 0, 0, 2, "9:Class Over")
        ringAt(17, 40, 0, 1, "1st Self-study Begin")
        ringAt(18, 40, 0, 2, "1st Self-study Over")
        ringAt(18, 50, 0, 1, "2nd Self-study Begin")
        ringAt(19, 50, 0, 2, "2nd Self-study Over")
        ringAt(20, 0, 0, 4, "3rd Self-study Begin")
        ringAt(22, 0, 0, 3, "3rd Self-study Over")
        pyExecAt(22, 0, 30, "shutitdown()")


if __name__ == "__main__":
    # 若直接运行
    # dailySchedule()
    infoLog("env", "OS:"+str(os.name)+" .")
    if os.name != "nt":
        infoLog("env", "CAUTION:Some functions may only work on Windows.")
        infoLog("env", "APP may crash on your OS.")
    argu = sys.argv
    infoLog("env", "Run with argv:"+str(argu)+".")
    if "showmsg" in argu:
        infoLog("env", "showmsg")
        showTextScript()
    elif "run" in argu:
        infoLog("env", "run")
        dailySchedule()
    elif "autoconvert" in argu:
        infoLog("env", "autoconvert")
        autoConvertScript()
    elif "console" in argu:
        infoLog("env", "console")
        console()
    elif "help" in argu or "/help" in argu or "-h" in argu or "--help" in argu or "/?" in argu or "-?" in argu or "?" in argu or "--h" in argu or "-help" in argu or "/h" in argu:
        infoLog("env", "help")
        infoLog(
            "HELP", "Available Args:run/(blank or anything not mentioned below)/showmsg [text]/autoconvert/console/help")
    elif "zwt" in argu:
        infoLog("env", "zwt")
        infoLog("env", "Easter Egg Found!")
        zwt()
    else:
        infoLog("env", "dailySchedule")
        dailySchedule()


if __name__ != "__main__":
    # 若被import
    infoLog("env", "OS:"+str(os.name)+" .")
    if os.name != "nt":
        infoLog("env", "CAUTION:Some functions may only work on Windows.")
        infoLog("env", "APP may crash on your OS.")
    infoLog("env", "Imported.")
    infoLog("env", "Hello from the AR Developer!")
    infoLog("HELP", "ringAt(hour,minute,second,stat,info)")
    infoLog("HELP", "stat:1-normBegin 2-normOver 3-AfterSchool 4-specBegin 5-specOver 6-NoSound")
    infoLog("HELP", "infoLog(origin,msg)")
    infoLog("HELP", "getSeconds(hour,minute,second)")
    infoLog("HELP", "playSound(filename)")
    infoLog("HELP", "pyExecAt(hour,minute,second,code)")
    infoLog("HELP", "showMsg(msg)")
    infoLog("HELP", "More functions available.Please read the source code.")


infoLog("env", "End of Script.")
