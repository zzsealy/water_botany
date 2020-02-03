import RPi.GPIO as GPIO
import time

channel = 2
data = []
j = 0

GPIO.setmode(GPIO.BCM)

time.sleep(1)

# 总线空闲状态为高电平，主机把总线拉低等待DHT11响应，主机把总线拉低必须大于18毫秒，
# 保证DHT11能检测到起始信号。
GPIO.setup(channel, GPIO.OUT) # 将引脚设为输出模式
GPIO.output(channel, GPIO.LOW) # 输出低电平
time.sleep(0.018)
# 主机发送开始信号后，可以切换到输入模式，或者输出高电平均可，总线由上拉电阻拉高。
GPIO.output(channel, GPIO.HIGH) # 输出高电平
GPIO.setup(channel, GPIO.IN) # 将引脚设为输入模式


while GPIO.input(channel) == GPIO.LOW:  # 读取引脚的输入状态
    continue
while GPIO.input(channel) == GPIO.HIGH:
    continue

while j < 40:
    k = 0
    while GPIO.input(channel) == GPIO.LOW:
        continue
    while GPIO.input(channel) == GPIO.HIGH:
        k += 1
        if k > 100:
            break
    if k < 8:
        data.append(0)
    else:
        data.append(1)

    j += 1

print("sensor is working.")
print(data)

humidity_bit = data[0:8]
humidity_point_bit = data[8:16]
temperature_bit = data[16:24]
temperature_point_bit = data[24:32]
check_bit = data[32:40]

humidity = 0
humidity_point = 0
temperature = 0
temperature_point = 0
check = 0

for i in range(8):
    humidity += humidity_bit[i] * 2 ** (7-i)
    humidity_point += humidity_point_bit[i] * 2 ** (7-i)
    temperature += temperature_bit[i] * 2 ** (7-i)
    temperature_point += temperature_point_bit[i] * 2 ** (7-i)
    check += check_bit[i] * 2 ** (7-i)

tmp = humidity + humidity_point + temperature + temperature_point

if check == tmp:
    print("temperature :", temperature, "*C, humidity :", humidity, "%")
else:
    print("wrong")
    print("temperature :", temperature, "*C, humidity :",
          humidity, "% check :", check, ", tmp :", tmp)

GPIO.cleanup()
