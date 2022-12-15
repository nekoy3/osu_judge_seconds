# coding: utf_8
import time

import picture
from draw_str import Draw

def main():
    picture.screenshot()
    img = picture.read_img()
    #判定タイミングエリア[[pixel, time], [], []]を取得

    area = picture.get_base_area(img)

    while True:
        #print(area)
        picture.screenshot()
        img = picture.read_img()
        picture.get_timing(area, img)
        #print(picture.get_timing_area(img))
        time.sleep(0.2)
        break

if __name__ == '__main__':
    main()