from flask import Flask
from config import Config
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from flask_mail import Mail 


moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() #handle login sessions 
#mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # tell my flask to use these services
    moment.init_app(app)
    db.init_app(app) 
    migrate.init_app(app, db) 
    login.init_app(app)
    #mail.init_app(app)
    



    with app.app_context():
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.blueprints.users import bp as users_bp
        app.register_blueprint(users_bp)

    return app