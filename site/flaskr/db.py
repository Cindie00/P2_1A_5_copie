##################################################################################################
#
#  ce fichier rempli la base de données vide (create_tables.sql) avec tous les fichiers insert_....sql
#  se trouvant dans le dossier sql
#
###################################################

## les imports
#
import sqlite3
import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

# cette fonction permet de se connecter à la base de données
#
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# cette fonction permet de fermer la base de données
#
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# cette fonction permet de vider toutes les tables de la base de données
#
def clear_db():
    db = get_db()
    with current_app.open_resource("sql/clear_tables.sql") as f:
        db.executescript(f.read().decode("utf8"))

#cette fonction rempli la base de données encore vide avec les fichiers insert....sql
#
def init_db():

    clear_db()

    db = get_db()

    # Creation des tables
    with current_app.open_resource("sql/create_tables.sql") as f:
        db.executescript(f.read().decode("utf8"))
    print("Tables crées")

    # Remplissage des tables
    fichiers = ['insert_animaux.sql', 'insert_animaux_types.sql', 'insert_animaux_velages.sql', 'insert_complications.sql', 'insert_familles.sql', 'insert_types.sql', 'insert_velages.sql', 'insert_velages_complications.sql']
    for index,fichier in enumerate(fichiers):
        emplacement = "sql/" + fichier
        with current_app.open_resource(emplacement) as f:
            db.executescript(f.read().decode("utf8"))
        print("Tables {}/{} remplies".format((index+1),len(fichiers)))
    print("Tables remplies")

    

# relie la commande flask init-db à la fonction init_db_command()
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


#cette fonction se lance lorsqu'on lance le site elle permet de relier la commande flask init-db
def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
