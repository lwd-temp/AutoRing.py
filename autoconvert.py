# 自助式自动化放学铃设置
import datetime
import json
import logging
import subprocess
import sys

# To disable functions.
#########################
# oped = 1
#########################

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='ac.log',
                    level=logging.DEBUG, format=LOG_FORMAT)

nowtime = datetime.datetime.now()
filename = str(nowtime.year)+str(nowtime.month)+str(nowtime.day) + \
    str(nowtime.hour)+str(nowtime.minute)+str(nowtime.second)+".mp3"
logging.info("Run")


# Call ffmpeg
def ffmpeg(infi, outfi):
    logging.info("ffmpeg "+str(infi)+" "+str(outfi))
    subprocess.call(["ffmpeg", "-i", str(infi), str(outfi)])
    logging.info("ffmpeg exit")


print("自助式自动化放学铃设置 Beta2坂本")
print("您的所有操作都将被记录备案，请不要恶意提交。")
# print("不一定需要重命名媒体文件为123并将其复制到桌面")


try:
    logging.info("Try to read json.")
    with open("music.json", "r") as data:
        filen = json.load(data)
    logging.info("Json exists.")
    with open(filen, "r") as testfile:
        logging.info("File exists.")
    print("已存在人工设置")
    logging.info("Operation exists.")
    oped = 1
except:
    logging.info("OK.")
    print("当前无人工设置")
    oped = 0

if oped == 1:
    print("当日已存在人工设置，为确保不覆写设置已禁止操作")
    print("按Enter退出程序")
    userinput = input()
    if userinput != "debug":
        sys.exit()
    else:
        print("Input Debugger Key:")
        dkr = str(nowtime.year+1)+str(nowtime.month*2)+str(nowtime.day+1)
        dk = input()
        if dk == dkr:
            logging.info("Hello,debugger!")
            print("Hello,debugger!")
            with open("music.json", "w") as data:
                data.write("init")
                logging.info("Json rewrite.")
                print("Json已覆写")
        else:
            print("Wrong")
            sys.exit()

fp = input("输入媒体文件路径或直接将文件拖入窗口并按下Enter：")
logging.info("用户输入："+fp)

print("用户输入："+fp)

# Fix cmd file dragging path complete feature
if fp[0] == '"':
    if fp[-1] == '"':
        fp = fp[1:-1]

logging.info("文件路径："+fp)

print("文件路径："+fp)

comment = input("输入本次提交描述并按Enter：")
logging.info("Comment:"+comment)

with open(fp, "r") as testfile:
    print("文件存在")
    logging.debug("File exists.")

print("调用ffmpeg，请注意错误信息")
ffmpeg(fp, filename)
print("转码结束，请注意错误信息")

try:
    with open(filename, "r") as testfile:
        logging.info("File ok.")
except:
    logging.info("File failed.")
    print("文件未生成，转码错误")
    sys.exit()

print("写入json")
logging.info("Try to write json.")
with open("music.json", "w") as data:
    json.dump(filename, data)

logging.info("Done")
print("完成，你可以安全地关闭窗口了。")
logging.info("Exit.")
