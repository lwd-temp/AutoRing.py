# AutoRing Project Audio Handler ar_audio.pyw
# 模拟学校上下课铃的程序 音频部分
# Version: stable--update 1
# Author:lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要第三方库pygame(Sound)
import time
import datetime
import pygame
import logging

# 初始化Pygame Mixer
pygame.mixer.init()

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
    track = pygame.mixer.music.load(file)
    infoLog("playSound", "Play "+file)
    pygame.mixer.music.play()


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


def getWeekday(date=datetime.datetime.now()):
    # 获取星期1-7
    day = date.weekday()
    intday = int(day)+1
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
        # 放学
        fn = "afterschool.mp3"
    return fn


def ringAt(hour, minute, second=0, stat=1, info="UNKNOWN"):
    # 响铃函数
    # stat 1 上课 2 下课 3 放学
    # 调用举例ringAt(12,12,14,2,"Test") 12:12:14 下课 日志信息"Test"
    # 超过12h跳过
    # 可以用多线程代替上述方案
    infoLog("ringAt", str(hour)+":"+str(minute)+":" +
            str(second)+" "+str(stat)+" "+str(info))
    passit = 0
    delta = getSeconds(hour, minute, second)
    infoLog("ringAt", "Delta "+str(delta))
    if delta >= 43200:
        passit = 1
        infoLog("ringAt", "Pass!")
    if passit == 0:
        infoLog("ringAt", "Sleeping...")
        time.sleep(delta)
        filename = getFilename(stat)
        playSound(filename)


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
        time.sleep(180)
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
        time.sleep(180)


def debugSchedule():
    # 测试用时间表
    infoLog("debugSchedule", "Debug!")
    if getWeekday() == 1:
        infoLog("debugSchedule", "Debug Monday")
        ringAt(0, 35, 0, 1, "Class Begin")
        ringAt(0, 35, 30, 2, "Class Over")
        ringAt(0, 36, 0, 3, "After School")
        time.sleep(180)
    else:
        infoLog("debugSchedule", "Debug NOT Monday")
        ringAt(0, 30, 0, 1, "Class Begin")
        ringAt(0, 31, 0, 2, "Class Over")
        ringAt(0, 32, 0, 3, "After School")
        time.sleep(180)


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