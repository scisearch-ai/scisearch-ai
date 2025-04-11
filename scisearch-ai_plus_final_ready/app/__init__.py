from flask import Flask
from .routes import app as routes_blueprint

def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(routes_blueprint)
    return flask_app
