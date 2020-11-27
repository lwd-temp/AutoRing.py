# 自助式自动化放学铃设置
import datetime
import json
import logging
import subprocess

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='ac.log',
                    level=logging.DEBUG, format=LOG_FORMAT)

nowtime = datetime.datetime.now()
filename = str(nowtime.year)+str(nowtime.month)+str(nowtime.day) + \
    str(nowtime.hour)+str(nowtime.minute)+str(nowtime.second)+".mp3"
logging.info("Run")


def ffmpeg(infi, outfi):
    logging.info("ffmpeg "+str(infi)+" "+str(outfi))
    subprocess.call(["ffmpeg", "-i", str(infi), str(outfi)])
    logging.info("ffmpeg exit")


print("自助式自动化放学铃设置 Beta坂本")
print("您的所有操作都将被记录备案，请不要恶意提交。")
print("重命名媒体文件为123并将其复制到桌面")
fp = input("输入媒体文件路径或直接将文件拖入窗口并按下Enter：")
logging.info(fp)
comment = input("输入本次提交描述并按Enter：")
logging.info("Comment:"+comment)

with open(fp, "r") as testfile:
    print("文件存在")
    logging.debug("File exists.")

print("调用ffmpeg")
ffmpeg(fp, filename)
print("转码结束")
print("写入json")
logging.info("Try to write json.")
with open("music.json", "w") as data:
    json.dump(filename, data)

logging.info("Done")
print("完成，你可以安全地关闭窗口了。")
logging.info("Exit.")
