from flask import Flask
from .database.db import mongo
from .routes import AuthRoutes, IndexRoutes, FileToFormatRoutes, Users

app = Flask(__name__)

def page_not_found(error):
    return "<h1>Pagina no encontrada</h1>"

def init_app(config):
    app.config.from_object(config)
    mongo.init_app(app)
    app.register_error_handler(404, page_not_found)
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/authentication')
    app.register_blueprint(Users.main, url_prefix='/api/users')
    app.register_blueprint(FileToFormatRoutes.main, url_prefix='/api/convert')
    return app
