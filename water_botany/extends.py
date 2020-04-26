from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail, Message

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manger = LoginManager()
login_manger.login_view = '/login' 

@login_manger.user_loader
def load_user(user_id):
    from water_botany.model import Admin
    user = Admin.query.get(int(user_id))
    return user