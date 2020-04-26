from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')

