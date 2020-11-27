# AutoRing Project Audio Handler ar_audio.pyw
# 模拟学校上下课铃的程序 音频部分
# Version: stable--update 2
# Author:lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要第三方库pygame(Sound)
import datetime
import json
import logging
import os
import random
import subprocess
import threading
import time

import pygame

# 初始化Pygame Mixer
pygame.mixer.init(buffer=10240)
# Bigger buffer to avoid strange sound effect when high I/O occures.

# 配置logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(origin)s] %(message)s"
logging.basicConfig(filename='ar_audio.log',
                    level=logging.DEBUG, format=LOG_FORMAT)


def infoLog(origin="UNKNOWN", msg="UNKNOWN"):
    # Info日志函数
    logging.info(str(msg), extra={'origin': str(origin)})
    print(str(origin)+":"+str(msg))


def playSound(filename="begin.mp3"):
    # 播放音乐filename
    file = str(filename)
    try:
        pygame.mixer.music.load(file)
        infoLog("playSound", "Play "+file)
        pygame.mixer.music.play()
    except:
        infoLog("playSound", "pygame.error!")
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


def getPass(hour, minute, second=0):
    # Get if pass
    # return 1 when pass
    # 获取是否已过当前时间
    nowtime = datetime.datetime.now()
    ifpass = 0
    if hour < nowtime.hour:
        ifpass = 1
    if hour == nowtime.hour:
        if minute < nowtime.minute:
            ifpass = 1
    if hour == nowtime.hour:
        if minute == nowtime.minute:
            if second < nowtime.second:
                ifpass = 1
    return ifpass


def getWeekday(date=datetime.datetime.now()):
    # 获取星期1-7
    day = date.weekday()
    intday = int(day)+1
    # Force Monday
    # intday = 1
    # End Force Monday
    # Force Normal
    # intday = 2
    # End Force Normal
    return intday


def getFilename(stat=2):
    # 根据事件获取文件名
    intstat = int(stat)
    fn = "alarm.mp3"
    if intstat == 1:
        # 上课
        fn = "begin.mp3"
    if intstat == 2:
        # 下课
        fn = "over.mp3"
    if intstat == 3:
        # 放学 在此保留Failsafe
        fn = "afterschool.mp3"
    return fn


def randPlaySound():
    # Random Music Player
    # 1.mp3 2.mp3 3.mp3 4.mp3 etc.
    # 随机播放音频
    # 文件名1.mp3 2.mp3 ...... 17.mp3
    randnum = random.randint(1, 30)
    # randnum = 17  # Force 17 强制“随机”
    randstr = str(randnum)
    fnstr = randstr+".mp3"
    infoLog("randPlaySound", fnstr)
    try:
        infoLog("json", "Try")  # 与autoconvert.py配合使用
        with open("music.json", "r") as data:
            filen = json.load(data)
        infoLog("json", str(filen))
        with open(filen, "r") as testfile:  # 检测文件存在性
            infoLog("chkfile", "File exists.")
        playSound(filen)
        with open("music.json", "w") as data:  # 覆写json使其失效
            data.write("init")
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
    infoLog("showMsgMain", "exit")


def showMsg(msg):
    # Threading to avoid waiting.
    # 多线程用于避免等待
    infoLog("showMsg", str(msg))
    ddd = threading.Thread(target=showMsgMain, args=[msg])
    ddd.start()


def altPlaySoundMain(file):
    # Call cmdmp3 to play sound.
    # In case of pygame.error
    # 调用cmdmp3.exe
    # 避免随机（？）出现的pygame.error影响播放
    infoLog("altPlaySoundMain", str(file))
    subprocess.call(["cmdmp3", str(file)])
    infoLog("altPlaySoundMain", "exit")


def altPlaySound(file):
    # Threading to avoid waiting.
    # 多线程
    infoLog("altPlaySound", str(file))
    ddd = threading.Thread(target=altPlaySoundMain, args=[str(file)])
    ddd.start()


def ringAt(hour, minute, second=0, stat=1, info="UNKNOWN"):
    # 响铃函数
    # stat 1 上课 2 下课 3 放学
    # 调用举例ringAt(12,12,14,2,"Test") 12:12:14 下课 日志信息"Test"
    # 可以用多线程代替上述方案
    infoLog("ringAt", str(hour)+":"+str(minute)+":" +
            str(second)+" "+str(stat)+" "+str(info))
    delta = getSeconds(hour, minute, second)
    infoLog("ringAt", "Delta "+str(delta))
    if getPass(hour, minute, second) == 1:
        infoLog("ringAt", "Pass!")
    else:
        infoLog("ringAt", "Sleeping...")
        time.sleep(delta)
        filename = getFilename(stat)
        stat = int(stat)
        # Delay to sync with the school timing
        # time.sleep(22)
        # F**k the stupid school timing system.
        if stat != 3:
            playSound(filename)
        if stat == 3:
            randPlaySound()
        showMsg(str(info))


def pyExecAt(hour, minute, second=0, code="print('No command.')"):
    # 在某时执行Python代码
    # 使用exec()
    # 调用举例pyExecAt(小时，分钟，秒，Python代码)
    infoLog("pyExecAt", str(hour)+":"+str(minute)+":" +
            str(second)+" "+str(code))
    delta = getSeconds(hour, minute, second)
    infoLog("pyExecAt", "Delta "+str(delta))
    if getPass(hour, minute, second) == 1:
        infoLog("pyExecAt", "Pass!")
    else:
        infoLog("pyExecAt", "Sleeping...")
        time.sleep(delta)
        infoLog("pyExecAt", "Exec")
        exec(code)


def shutitdown():
    # 关机操作
    os.system("shutdown -s -t 600")  # 10分钟定时关机
    time.sleep(10)  # 等待执行和GUI提示
    os.system("rundll32.exe user32.dll,LockWorkStation")  # 锁定工作站
    time.sleep(540)  # 等待音乐播放完成退出程序 9分钟


def dailySchedule():
    # 标准时间表
    if getWeekday() == 1:
        # 若周一
        infoLog("dailySchedule", "Today is Monday")
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
        ringAt(13, 30, 0, 1, "6:Class Begin")
        ringAt(14, 10, 0, 2, "6:Class Over")
        ringAt(14, 20, 0, 1, "7:Class Begin")
        ringAt(15, 0, 0, 2, "7:Class Over")
        ringAt(15, 30, 0, 1, "8:Class Begin")
        # ringAt(16,10,0,2,"8:Class Over")
        # ringAt(16,20,0,1,"9:Class Begin")
        # Removed those ringAt due to the user's request.
        ringAt(17, 0, 0, 2, "9:Class Over")
        ringAt(17, 40, 0, 1, "1st Self-study Begin")
        ringAt(18, 40, 0, 2, "1st Self-study Over")
        ringAt(18, 50, 0, 1, "2nd Self-study Begin")
        ringAt(19, 50, 0, 2, "2nd Self-study Over")
        ringAt(20, 0, 0, 1, "3rd Self-study Begin")
        ringAt(22, 0, 0, 3, "3rd Self-study Over")
        pyExecAt(22, 0, 30, "shutitdown()")
    elif getWeekday() == 7:
        # 若周日
        infoLog("dailySchedule", "Today is Sunday.")
##        ringAt(8, 20, 0, 2, "1Sun:Over")
##        ringAt(8, 30, 0, 1, "2Sun:Begin")
##        ringAt(10, 0, 0, 2, "3Sun:Over")
##        ringAt(10, 30, 0, 1, "3Sun:Begin")
        ringAt(12, 0, 0, 3, "SchoolOver")
        pyExecAt(12, 0, 30, "shutitdown()")
    else:
        infoLog("dailySchedule", "Today is NOT Monday")
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
        ringAt(13, 30, 0, 1, "6:Class Begin")
        ringAt(14, 10, 0, 2, "6:Class Over")
        ringAt(14, 20, 0, 1, "7:Class Begin")
        ringAt(15, 0, 0, 2, "7:Class Over")
        ringAt(15, 30, 0, 1, "8:Class Begin")
        # ringAt(16,10,0,2,"8:Class Over")
        # ringAt(16,20,0,1,"9:Class Begin")
        # Removed those ringAt due to the user's request.
        ringAt(17, 0, 0, 2, "9:Class Over")
        ringAt(17, 40, 0, 1, "1st Self-study Begin")
        ringAt(18, 40, 0, 2, "1st Self-study Over")
        ringAt(18, 50, 0, 1, "2nd Self-study Begin")
        ringAt(19, 50, 0, 2, "2nd Self-study Over")
        ringAt(20, 0, 0, 1, "3rd Self-study Begin")
        ringAt(22, 0, 0, 3, "3rd Self-study Over")
        pyExecAt(22, 0, 30, "shutitdown()")


# def debugSchedule():
# 测试用时间表
##    infoLog("debugSchedule", "Debug!")
# if getWeekday() == 1:
##        infoLog("debugSchedule", "Debug Monday")
##        ringAt(0, 35, 0, 1, "Class Begin")
##        ringAt(0, 35, 30, 2, "Class Over")
##        ringAt(0, 36, 0, 2, "After School")
# time.sleep(180)
# else:
##        infoLog("debugSchedule", "Debug NOT Monday")
##        ringAt(0, 30, 0, 1, "Class Begin")
##        ringAt(0, 31, 0, 2, "Class Over")
##        ringAt(0, 32, 0, 2, "After School")
# time.sleep(180)


if __name__ == "__main__":
    # 若直接运行
    dailySchedule()

if __name__ != "__main__":
    # 若被import
    infoLog("env", "Imported")
    infoLog("HELP", "ringAt(hour,minute,second,stat,info)")
    infoLog("HELP", "stat:1-Begin 2-Over 3-AfterSchool")
    infoLog("HELP", "infoLog(origin,msg)")
    infoLog("HELP", "getSeconds(hour,minute,second)")
    infoLog("HELP", "playSound(filename)")
    infoLog("HELP", "pyExecAt(hour,minute,second,code)")
    infoLog("HELP", "showMsg(msg)")
