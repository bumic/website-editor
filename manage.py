from flask_script import Manager
from app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def run():
    #  $ python -m flask run
    app.run(port=4996)

@manager.command
def test():
    pass
