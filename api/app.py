from flask import Flask, jsonify
from config import Config
from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(api)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "fintrack-api"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)