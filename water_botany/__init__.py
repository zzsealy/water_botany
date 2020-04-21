from flask import Flask, render_template, Response, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345wsfs'
bootstrap = Bootstrap(app)
 
# Raspberry Pi camera module (requires picamera package)
from water_botany.camera_pi import Camera
from water_botany.realy import start_realy
import Adafruit_DHT
import time
 

# 从dht22温湿度传感器获取数据
def getDHTdata():       
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
     
    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum

 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_realy(3)
    timeNow = time.asctime( time.localtime(time.time()) )
    temp, hum = getDHTdata()
     
    templateData = {
      'time': timeNow,
      'temp': round(temp/25.1, 1),
      'hum' : round(hum/25.1, 1)
    }
    return render_template('index.html', templateData=templateData)
 
@app.route('/camera')
def cam():
    """视频页面"""
    timeNow = time.asctime( time.localtime(time.time()) )
    templateData = {
      '时间': timeNow
    }
    return render_template('camera.html', **templateData)

 
def gen(camera):
    """视频流生成函数"""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
 
@app.route('/video_feed')
def video_feed():
    """ 视频流路由，嵌入到src里 """
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
