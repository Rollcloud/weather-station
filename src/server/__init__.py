import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from . import db, weather


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "weather.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register init functions from db.py with the app
    # https://flask.palletsprojects.com/en/3.0.x/tutorial/database/#register-with-the-application
    db.init_app(app)

    # register weather blueprint with the app
    app.register_blueprint(weather.bp)
    app.add_url_rule("/", endpoint="index")

    return app

def connect_middleware(app):
    app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    return app

# See https://stackoverflow.com/a/51397334
if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    app = create_app()
    gunicorn_app = connect_middleware(app)