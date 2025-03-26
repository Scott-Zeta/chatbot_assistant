from flask import Flask
from flask_cors import CORS
from config.settings import Config

def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, **Config.CORS_SETTINGS)
    
    # Update session cookie settings
    app.config.update(**Config.SESSION_COOKIE_SETTINGS)
    
    # Register blueprints
    from app.routes.chat_routes import chat_bp
    from app.routes.contact_routes import contact_bp
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(contact_bp)
    
    return app