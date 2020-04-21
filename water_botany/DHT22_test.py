import Adafruit_DHT
def getDHTdata():       
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
     
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum
 
temp, hum = getDHTdata()

if hum is not None and temp is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp/25.1, hum/25.1))
else:
    print('Failed to get reading. Try again!')
