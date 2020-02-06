# encoding=utf-8
 
import RPi.GPIO as GPIO
import time
 
# 延时函数
def delay(i):
    while i:
        i -= 1
 
# 初始化dht11连接引脚
# dht11_pin - dht11连接的引脚号
def init_dht11(dht11_pin):
    # 输出模式 初始状态给高电平
    GPIO.setup(dht11_pin, GPIO.OUT)
    GPIO.output(dht11_pin, 1)
 
# 用于获取
# dht11_pin - dht11连接的引脚号
# 返回二元组 [ 湿度 , 温度 ]
def get_dht11(dht11_pin):
    buff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
 
    GPIO.output(dht11_pin,0)
    time.sleep(0.02)                    # 拉低20ms
 
    GPIO.output(dht11_pin,1)
 
    GPIO.setup(dht11_pin,GPIO.IN)        # 这里需要拉高20-40us,但更改模式需要50us,因此不调用延时
 
 
    while not GPIO.input(dht11_pin):    # 检测返回信号 检测到启示信号的高电平结束
        pass
 
 
    while GPIO.input(dht11_pin):        # 检测到启示信号的高电平则循环
        pass
 
    i=40
 
    while i:
        start=time.time()*1000000        # 为了严格时序 循环开始便计时
        i-=1
        while not GPIO.input(dht11_pin):
            pass
        while GPIO.input(dht11_pin):
            pass
        buff[i]=time.time()*1000000-start# 为了严格时序 每次测得数据后都不马上处理 先存储
 
    GPIO.setup(dht11_pin,GPIO.OUT)        # 读取结束 复位引脚
    GPIO.output(dht11_pin,1)
 
    # print "buff - ",buff
 
    # 开始处理数据
    for i in range(len(buff)):            # 将时间转换为 0 1
        if buff[i]>100:                    # 上方测试时是测试整个位的时间
                                        # 因此是与100比较 大于100为1(位周期中 低电平50us)
            buff[i]=1
        else:
            buff[i]=0
    # print "After - ",buff
 
    i=40
    hum_int=0
    while i>32:                # 湿度整数部分
        i-=1
        hum_int<<=1
        hum_int+=buff[i]
    # print "hum - ",hum_int
 
    tmp_int=0
    i=24
    while i>16:                # 温度整数部分
        i-=1
        tmp_int<<=1
        tmp_int+=buff[i]
    # print "tmp - ",tmp_int
    return [hum_int,tmp_int]
 
GPIO.setmode(GPIO.BOARD)
init_dht11(7)
print get_dht11(7)
GPIO.cleanup()
 
# 注意
# 若非连续测量 可以不延时 但连续测量时建议每次测量间间隔0.2s以上再调用get_dht11(dht11_pin)获取数据(树莓派不稳定)
# DHT11虽然有40位 实际温度和湿度的小数部分读数总为0
# 如果程序无法正常读取，可以考虑是否起始部分的延时不准确，可以参考注释以及实际环境的测量结果调整延时
# 程序测试环境为 $树莓派3代B+$ $python2.7.9 $Raspbian GNU/Linux 8$
