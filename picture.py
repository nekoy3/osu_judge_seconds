#https://qiita.com/meznat/items/c3350e85da1d3157360a

import mss
import mss.tools
import cv2
import matplotlib.pyplot as plt
import time

filename = "sct.png"
SCREEN_HEIGHT=1080
SCREEN_WIDTH=1920

#スクリーンショットを撮影
def screenshot(monitor_number = 0, output=filename):
    with mss.mss() as sct:
        output = sct.shot(mon=monitor_number, output=output)

#画像ファイルを読み込む
def read_img(filename =filename):
    return cv2.imread(filename)

#画像ファイルを表示する（検証用）
def show_img(img):
    #matplotlibで表示する場合はRGBからBGRに変換
    img = cv2.cvtColor( img, cv2.COLOR_RGB2BGR)
    plt.imshow(img)
    plt.show()

#トリムする判定タイミングエリアを取得 y=1063, x=960
def get_timing_area(img):
    center = [int(SCREEN_HEIGHT*0.985), int(SCREEN_WIDTH*0.5)]

    screenshot()
    img = read_img()
    trim_area = img[center[0], center[1]:center[1]+300]
    white = 0
    t300, t100, t50 = 0, 0, 0
    for i, rgb in enumerate(trim_area):
        #白（中央ライン）はパス
        if rgb[0] > 250 and rgb[1] > 250 and rgb[2] > 250:
            white=i
        #水色（300判定）
        elif rgb[0] == 231 and rgb[1] == 188 and 75 > rgb[2] == 50:
            t300=i
        #緑（100判定）
        elif rgb[0] == 19 and rgb[1] == 227 and rgb[2] == 87:
            t100=i
        #黄（50判定）
        elif rgb[0] == 70 and rgb[1] == 174 and rgb[2] == 218:
            t50=i
        #判定ライン終了でbreak(出来なくても処理時間以外に影響はない)
        elif rgb[0] < 30 and rgb[1] < 30 and rgb[2] < 30:
            continue
    t300 -= white
    t100 -= white
    t50 -= white
    #timing = [t300, t100, t50]
    #ただしOD6~10での値である
    timing = [[round(t300*0.90249, 1)], [round(t100*0.89355, 1)], [round(t50*0.887405, 1)]]
    timing[0].append(t300)
    timing[1].append(t100)
    timing[2].append(t50)
    return timing