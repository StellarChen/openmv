# Untitled - By: chen yuxin - 周二 9月 24 2019

import sensor, image, time, pyb, math
from pyb import UART
red_threshold = (30, 86, 28, 97, -47, 92)
green_threshold  = (45, 97, -88, -25, -69, 96)
blue_threshold  = (74, 90, -29, 5, -59, -4)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()
uart = UART(3,9600)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
        return max_blob
def find_maxsize(size1,size2,size3):
    if size1>size2:
        if size1>size3:
            return 1
        else :
            return 3
    else :
        if size2>size3:
            return 2
        elif size3>size2 :
            return 3
size11=0
size21=0
size31=0
while(True):
    clock.tick()
    img = sensor.snapshot()
    #lens_corr(1.8)畸变矫正
    blob1=img.find_blobs([red_threshold], pixels_threshold=700, area_threshold=700,merge=True)
    if blob1:
        max_blob1=find_max(blob1)
        size11=max_blob1[2]*max_blob1[3]
    blob2=img.find_blobs([green_threshold], pixels_threshold=700, area_threshold=700,merge=True)
    if blob2:
        max_blob2=find_max(blob2)
        size21=max_blob2[2]*max_blob2[3]
    blob3=img.find_blobs([blue_threshold], pixels_threshold=700, area_threshold=700,merge=True)
    if blob3:
        max_blob3=find_max(blob3)
        size31=max_blob3[2]*max_blob3[3]
    num=find_maxsize(size11,size21,size31)
    if num==1:
        img.draw_cross(max_blob1.cx(), max_blob1.cy(),color = (176,48,96))
        uart.write('1')
        print('1')
    elif num==2:
        img.draw_cross(max_blob2.cx(), max_blob2.cy(),color = (34,139,34))
        uart.write('2')
        print('2')
    elif num==3:
        img.draw_cross(max_blob3.cx(), max_blob3.cy(),color = (0,0,128))
        uart.write('3')
        print('3')


    uart.write('\n')
    #print(clock.fps())
