#https://qiita.com/meznat/items/c3350e85da1d3157360a

import mss
import mss.tools
import cv2
import matplotlib.pyplot as plt
import time

filename = "sct.png"
SCREEN_HEIGHT=1080
SCREEN_WIDTH=1920
center = [int(SCREEN_HEIGHT*0.985), int(SCREEN_WIDTH*0.5)]
white = 0
timing_color = {'t300': [0,0,0], 't100': [0,0,0], 't50': [0,0,0]}

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
    global white
    img = read_img()
    trim_area = img[center[0], center[1]:center[1]+300]
    t300, t100, t50 = 0, 0, 0
    tmp = [0, 0, 0]
    t_cnt = 0 #300 - 100 - 50 -> 0 - 1 - 2
    on_start = True
    for i, rgb in enumerate(trim_area):
        rgb = list(rgb) #numpy配列なのでlistに変換
        #白（中央ライン）はパス
        if rgb[0] == rgb[1] == rgb[2] and on_start:
            white=i
            continue
        #異常値ならreturn
        elif white == 0 and on_start:
            return
        #初回ならtmpに格納してcontinueする
        elif on_start:
            tmp = rgb
            on_start = False
            print("on_start")
            continue
        
        #水色（300判定） 
        if t_cnt == 0 and tmp == rgb:
            continue
        elif list(trim_area[i+4]) == rgb: #判定により色が変わった場合の誤認式の場合は防ぐ
            continue
        elif t_cnt == 0: 
            timing_color['t300'] = rgb
            tmp = rgb
            t_cnt += 1
            t300 = i

        #緑（100判定）
        if t_cnt == 1 and tmp == rgb:
            continue
        elif list(trim_area[i+4]) == rgb: #判定により色が変わった場合の誤認式の場合は防ぐ
            continue
        elif t_cnt == 1:
            timing_color['t100'] = rgb
            tmp = rgb
            t_cnt += 1
            t100 = i

        #黄（50判定）
        if t_cnt == 2 and tmp == rgb:
            continue
        elif list(trim_area[i+4]) == rgb: #判定により色が変わった場合の誤認式の場合は防ぐ
            continue
        elif t_cnt == 2:
            timing_color['t50'] = rgb
            t50 = i
        
        #判定ライン終了でbreak(出来なくても処理時間以外に影響はない)
        if rgb[0] < 10 and rgb[1] < 10 and rgb[2] < 10:
            break
    
    t300 -= white
    t100 -= white
    t50 -= white
    #timing = [t300, t100, t50]
    #ただしOD6~10での値である
    timing = [[round(t300*0.90249, 1)], [round(t100*0.89355, 1)], [round(t50*0.887405, 1)]]
    timing[0].append(t300)
    timing[1].append(t100)
    timing[2].append(t50)
    print(timing)
    print(timing_color)
    return timing

#繰り返し確認してベースが確定したらareaを返す
def get_base_area(img):
    area = get_timing_area(img)
    
    cnt=0
    while True:
        time.sleep(0.1)
        area_tmp = get_timing_area(img)
        if cnt == 10:
            break
        elif area == area_tmp:
            cnt+=1
        else:
            cnt=0
            area = area_tmp

    return area

#判定タイミング誤差を取得
def get_timing(area, img):
    global white
    trim_arrow = img[int(center[0]-10), int(center[1]-area[2][1]-(white/2)):int(center[1]+area[2][1]+(white/2))]
    start = int(center[1]-area[2][1]-(white/2))
    end = int(center[1]+area[2][1]+(white/2))

    trim_area = img[center[0]-10:center[0]+3, start:end]
    #trim_area = img[center[0]-10:center[0]+10, center[1]-10:center[1]+10]
    #show_img(trim_area)
    
    print(start)
    print(end)
    #for i in range(len(trim_arrow)):
    #    if trim_arrow[i]

    #中央から±20pixelを許容するものとする
    for i, rgb in enumerate(trim_arrow):
        pos = center[1] - int(len(trim_arrow)/2) + i + 10
        #print("pos " + str(pos) + str(set(rgb) == set([255, 255, 255])) + " " + str(center[1]+20 < pos or pos < center[1]-20))
        #誤差があると判断
        if set(rgb) == set([255, 255, 255]) and center[1]+20 < pos > center[1]-20:
            if center[1]+20 < pos < center[1]+area[0][1] or center[1]-20 > pos > center[1]-area[0][1]:
                print("300 " + str(int(i-len(trim_arrow)/2)*0.90249))
            elif center[1]+area[1][1] > pos > center[1]+area[0][1] or center[1]-area[0][1] < pos < center[1]-area[1][1]:
                print("100 " + str(int(i-len(trim_arrow)/2)*0.89355))
            elif center[1]+area[2][1] > pos > center[1]+area[1][1] or center[1]-area[1][1] < pos < center[1]-area[2][1]:
                print("50 " + str(int(i-len(trim_arrow)/2)*0.887405))
            #else:
                #print("error " + str(i) + " " + str(pos))
            #print("center " + str(center))
            break
            
    