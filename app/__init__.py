from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    # Inicialización
    db.init_app(app)
    migrate.init_app(app, db)
    

    # Registro de Blueprints
    from app.routes.registration import registration_bp
    app.register_blueprint(registration_bp)

    from app.routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.routes.info import info_bp
    app.register_blueprint(info_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('under_development.html'), 404
    
    return app
