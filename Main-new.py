
import time
from math import *
from decimal import Decimal

from fpsdetect import *
from ctypes import *
from utils.fpsutils import *

import threading

import pyautogui
import win32api
import win32con

from utils.metrics import ConfusionMatrix

is_screen = False

class ScreenThread(threading.Thread):
    def  __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global is_screen
        while True:
            if is_screen is True:
                screenShot()

def screenShot():

    img = pyautogui.screenshot(region=[0,0,1920,1080])



if __name__ == "__main__":
    while True:
        try:
            img = ScreenShot()
            detections = detect(img)
            btc = FindBestCenter(detections)
            x = btc[0] - ScreenShot_W // 2
            y = btc[1] - ScreenShot_H // 2

            print(x,y,btc[0],btc[1])
            if btc is not None:
                is_screen = True

                #cod16
                # import pydirectinput 
                # pydirectinput.move(x,y)

                #CF，CSGO，
                # win32api.keybd_event(17,0,0,0)
                # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
                # time.sleep(0.2)

                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x,y,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


                
                


        except:
            #print('No detect !')
            pass
