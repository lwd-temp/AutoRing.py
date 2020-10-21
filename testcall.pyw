import subprocess
import threading
def mainfunc(msg):
    subprocess.call(["pythonw", "showtext.pyw", msg])

def show(msg):
    ddd=threading.Thread(target=mainfunc,args=[msg])
    ddd.start()

show("TEST")
print("done")