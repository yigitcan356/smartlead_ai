from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from app.database import init_db
from app.routes import page_bp, api_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    with app.app_context():
        init_db(app)

    app.register_blueprint(page_bp)
    app.register_blueprint(api_bp)

    @app.get("/health")
    def health():
        return jsonify({
            "basari": True,
            "durum": "calisiyor"
        }), 200

    return app