#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import time

channel = 21 #管脚40，参阅树莓派引脚图，物理引脚40对应的BCM编码为21
channel2 = 20 # 控制继电器高低电平的引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel2, GPIO.IN)
GPIO.setup(channel2, GPIO.OUT)

while True:
        if GPIO.input(channel) == GPIO.LOW:
                print "土壤检测结果：潮湿"
                print(GPIO.input(channel2))
                GPIO.output(channel2, GPIO.LOW)
        else:
                print "土壤检测结果：干燥"
                print(GPIO.input(channel2))
                GPIO.output(channel2, GPIO.HIGH)
        time.sleep(1)
