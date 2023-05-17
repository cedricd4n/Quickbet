from flask import Flask
import os


from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_admin import helpers as admin_helpers
# from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore, UserMixin

from flask_redis import FlaskRedis
from flask_mail import Mail
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView


from flask_admin import Admin
socketio = SocketIO()
csrf = CSRFProtect()
redis_store = FlaskRedis()
migrate = Migrate()
admin = Admin(name='Quickcash')
mail1=Mail()
db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(debug=False):
    from  app.models import User
    
    from flask_session import Session
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir}/application.db"
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:://admin:r00tmysql@database.ce6yjppkl8ml.us-east-1.rds.amazonaws.com:3306/database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE']='filesystem'
    app.config['MAIL_SERVER']='smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'cashq261@gmail.com'
    app.config['MAIL_PASSWORD'] = 'lyzffnwlockyqhyk'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['REDIS_URL'] = 'redis://localhost:6379/0'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['FLASK_ADMIN_TEMPLATE_MODE'] = 'bootstrap3'
    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
    app.config['FLASK_ADMIN_BASE_TEMPLATE'] = 'admin/master.html'
    socketio.init_app(app,async_mode=None, logger=True, engineio_logger=True)
    csrf.init_app(app)
    db.init_app(app)
    mail1.init_app(app)
    admin.init_app(app)
    redis_store.init_app(app)
    migrate.init_app(app,db)
    login_manager= LoginManager()

    login_manager.login_view='auth.login'
    login_manager.login_message='Veuillez vous connecter pour accéder à cette page'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        
        return User.query.get(int(user_id))
    with app.app_context():
        
        
        from .main import main
        app.register_blueprint(main)
        from .auth import auth
        app.register_blueprint(auth)
        from .mail import mails
        app.register_blueprint(mails)
        from .admin import admin_bp
        app.register_blueprint(admin_bp)

        
        return app

