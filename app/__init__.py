from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.member import Member
    from app.models.household import Household
    from app.models.chore import Chore

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import chores_bp
    app.register_blueprint(chores_bp)

    from .routes import households_bp
    app.register_blueprint(households_bp)

    from .routes import members_bp
    app.register_blueprint(members_bp)

    CORS(app)
    return app