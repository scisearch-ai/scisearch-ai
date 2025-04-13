# main.py
from flask import Flask
from app.routes import app as routes_blueprint

app = Flask(__name__, template_folder="app/templates")
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
