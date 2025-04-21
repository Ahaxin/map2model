from flask import Flask, render_template
from app.api.routes import api

def create_app():
    app = Flask(__name__, template_folder="../templates")  # <- important!
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
