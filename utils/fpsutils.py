
import math
import pyautogui
import  numpy as np


Screen_W = 1920
Screen_H = 1080
Screen_Center_X = Screen_W // 2
Screen_Center_Y = Screen_H // 2 # is [960,540]
Screen_Center = [960,540]
ScreenShot_W = 416
ScreenShot_H = 416
Frame_X = (Screen_W - ScreenShot_W)// 2
Frame_Y = (Screen_H - ScreenShot_H) // 2 

print(Frame_X,Frame_Y,Screen_Center)

def ScreenShot():
    img = pyautogui.screenshot(region=[Frame_X,Frame_Y,ScreenShot_W,ScreenShot_H])
    return np.array(img)

def Center(p):
    return [p[0] + p[2] //2 , p[1] + p[3] // 2]

def Distence(a,b):
    return math.sqrt(
        ((a[0] - b[0])** 2) + ((a[1] - b[1]) ** 2)
    ) 
def FindBestCenter(detections):
    ch = {'p': [0,0,0,0], 'd': float('inf'),'c': 0.0 }
    for dt in detections:
        if dt['conf'] > 0.81:
            dt_p = dt['position']
            dt_c = Center(dt_p)
        if dt['class'] == 'person':
            dt_d = Distence(dt_c,Screen_Center)
            if dt_d < ch['d']:
                ch['p'] = dt['position']
                ch['d'] = dt_d
                ch['c'] = dt['conf']
                pass
    if ch['d'] != float('inf'): 
        btc = Center(ch['p'])
        return btc
    return None,None