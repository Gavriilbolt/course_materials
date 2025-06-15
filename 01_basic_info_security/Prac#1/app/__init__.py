from flask import Flask
from .config import Config
from .extensions import db, migrate
from .admin.views import admin_bp
from .comments.views import comments_bp
from .main.views import main_bp  



def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(comments_bp, url_prefix='/comments')

    app.register_blueprint(main_bp)


    return app