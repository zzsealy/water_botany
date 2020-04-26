from flask import Flask, render_template, Response, redirect, url_for, flash, request
from water_botany.extends import db, bootstrap, login_manger, mail
import os
import click
from flask_login import login_user, logout_user, login_required, current_user
from water_botany.model import Admin
from water_botany.form import LoginForm
# Raspberry Pi camera module (requires picamera package)
from water_botany.camera_pi import Camera
from water_botany.realy import start_realy
import Adafruit_DHT
import time
from flask_mail import Message
from water_botany.config import Config
import json


def create_app():
    app = Flask('water_botany')
    app.config.from_object(Config)
    Config.init_app(app)
    register_extends(app)
    register_shell_context(app)
    register_admin(app)
    return app




# 初始化扩展
def register_extends(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manger.init_app(app)
    mail.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin)

def register_admin(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            db.drop_all()
            click.echo('删除了数据库')
        db.create_all()
        click.echo('创建了数据库')
        admin = Admin(username="admin", password="123456")
        db.session.add(admin)
        db.session.commit()
        click.echo("创建管理员，账号admin, 密码123456")
    
def send_email(temp, hum):
    msg = Message('树莓派监控邮件', sender=os.environ.get('MAIL_USERNAME'), recipients=['zzsealy@qq.com'])
    msg.body = '温湿度检测'
    msg.html = '温度是:{}摄氏度, 湿度是:{}%'.format(temp, hum)
    try:
        with app.app_context():
            mail.send(msg)
            print('已经发送邮件')
    except:
        flash('发生错误')

# 从dht22温湿度传感器获取数据
def getDHTdata():
    DHT22Sensor = Adafruit_DHT.DHT22
    DHTpin = 16
    hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)

    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum


app = create_app()



@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    timeNow = time.asctime(time.localtime(time.time()))
    temp, hum = getDHTdata()

    temp = round(temp/25.1, 1)
    hum = round(hum/25.1, 1)
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        if data['ok'] == 1:
            start_realy(3)
        elif data['ok'] == 2:
            print("运行到这里")
            send_email(temp, hum)
            print('运行结束')
    

    templateData = {
      'time': timeNow,
      'temp': temp,
      'hum': hum
    }
    return render_template('index.html', templateData=templateData)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(u'你已经登陆了！', 'info')
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and password == admin.password:
                login_user(admin, remember)
                flash('登陆成功', 'info')
                return redirect('/')
            flash('账号密码错误', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'退出登录', 'info')
    return redirect('/')




@app.route('/camera')
def cam():
    """视频页面"""
    timeNow = time.asctime(time.localtime(time.time()))
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


