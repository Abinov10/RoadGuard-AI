"""
RoadGuard AI – Tamil Nadu Climate-Aware Road Risk Monitoring System
Main Flask Application Entry Point
"""
import os
from flask import Flask
from flask_cors import CORS

from db import ensure_indexes

# Blueprint imports (routes)
from routes.upload import upload_bp
from routes.detections import detections_bp
from routes.admin import admin_bp
from routes.api import api_bp


def create_app():
    """Application factory."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    # Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "roadguard-ai-secret-key-change-in-production")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")
    
    # Ensure upload directories exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    CORS(app)
    
    # Blueprints
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(detections_bp, url_prefix="/detections")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        from flask import render_template
        from db import TAMIL_NADU_DISTRICTS
        return render_template("index.html", districts=TAMIL_NADU_DISTRICTS)
    
    # Initialize DB indexes on startup
    with app.app_context():
        try:
            ensure_indexes()
        except Exception:
            pass  # MongoDB may not be running in dev
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
