from flask import Flask, request, jsonify
from extensions import db, login_manager
from auth.routes import auth_bp
from bot.chat_routes import chat_bp
from auth.models import User, SearchHistory, Product
from bot.nlp_module import process_user_message

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app  # Ensure the app is returned from create_app

# The main entry point of the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
