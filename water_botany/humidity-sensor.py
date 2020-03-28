#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time
        


def start_realy(num):
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(20,GPIO.OUT)    
    GPIO.output(20,GPIO.LOW)

    print("开始浇水")
    GPIO.cleanup()
    time.sleep(num)
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(20,GPIO.OUT)    
    GPIO.output(20,GPIO.LOW)
    print("浇水结束")


channel = 21 #管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

while True:
        if GPIO.input(channel) == GPIO.LOW:
                print("土壤检测结果：潮湿")
        else:
                print("土壤检测结果：干燥")
                start_realy(3)
        time.sleep(1)
