# coding: utf_8
import time

import picture

def main():
    img = picture.read_img()
    #判定タイミングエリア[[pixel, time], [], []]を取得
    area = picture.get_timing_area(img)
    while True:
        print(picture.get_timing(area, img))
        time.sleep(1)

if __name__ == '__main__':
    main()