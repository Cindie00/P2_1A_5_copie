################################################################################################
#
#  fichier "princicpal" du site, ce fichier crée une instance de l'application flask
#
##########################################################################

## Les imports
#
import os
from flask import Flask

## crée une instance de l'application flask
#
def create_app(test_config=None):
    """
    pre:/
    post: une instance de l'application flask (app)
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db
    db.init_app(app)

    from flaskr import index

    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    return app
