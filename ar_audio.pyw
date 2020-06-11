# AutoRing.pyw Audio
# 模拟学校上下课铃的程序
# Author:lwd-temp
# https://github.com/lwd-temp/AutoRing.py
# 需要库pygame(Sound)
import time
import datetime
import pygame
 
pygame.mixer.init()
 
stcuti=datetime.datetime.now()
strstcuti=str(stcuti.year)+"-"+str(stcuti.month)+"-"+str(stcuti.day)+"-"+str(stcuti.hour)+"-"+str(stcuti.minute)+"-"+str(stcuti.second)
logname="AutoRingAudioLog-"+strstcuti+".txt"
 
def logit(msg):
    # 日志函数
    print(str(msg))
    with open(logname,"a") as logfile:
        content="["+str(datetime.datetime.now())+"]"+str(msg)+"\n"
        logfile.write(content)
 
def playsound():
    # 播放音乐alarm.mp3
    file="alarm.mp3"
    track = pygame.mixer.music.load(file)
    logit("[PlaySound]Play")
    pygame.mixer.music.play()
 
logit("!!!!!!本次日志开始!!!!!!")
logit("Audio日志文件"+logname)
 
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
    # 在某时提醒，超过2h不提醒
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
    if delta>=7200:
        passit=1
        logit("[RingAt]Pass")
    if passit==0:
        logit("[RingAt]Sleeping...")
        time.sleep(delta)
        playsound()
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
time.sleep(32) # Sleep for 32s to make sure that the music has been played.
 
logit("Work done.Program Exit.")
