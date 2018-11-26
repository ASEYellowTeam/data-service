import os
from flask import Flask
from konfig import Config
from flakon.blueprints import SwaggerBlueprint, JsonBlueprint
from dataservice.database import db, User, Run, Objective, Challenge
from flask_sqlalchemy import SQLAlchemy

# This definition of the creation of the app is from flakon
# it is important for allowing the recognition of yaml file
def create_app(name=__name__, blueprints=None, settings=None):
    app = Flask(name)

    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataservice.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # load configuration
    settings = os.environ.get('FLASK_SETTINGS', settings)
    if settings is not None:
        app.config_file = Config(settings)
        app.config.update(app.config_file.get_map('flask'))

    # Create the SqlAlchemy db instance
    #db = SQLAlchemy(app)

    # register blueprints
    if blueprints is not None:
        for bp in blueprints:
            app.register_blueprint(bp)

    #Init database
    db.init_app(app)
    db.create_all(app=app)
    return app

def main():
    app = create_app()
    app.run(host="0.0.0.0",port=5002,debug=True)


if __name__ == '__main__':
    main()
