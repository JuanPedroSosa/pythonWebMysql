from app import create_app

#esto par usar el shell
from app import db, User, Task

#importamos el shell
from flask_script import Manager, Shell

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from config import config

cofig_class = config["development"]
# es singletone = se crea una sola instancia
app = create_app(cofig_class)

migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Task=Task)

if __name__ == "__main__":
	manager= Manager(app)

	# usar comandos desde el shell de python
	manager.add_command("shell", Shell(make_context=make_shell_context))
	# para realizar migraciones debemos ejecutar
	# 1. python manage.py db init
	# 2. python manage.py db migrate
	# 3. python manage.py db upgrade aplicar los cambios a la base
	# cada vez que hacemos un cambio ejecutar punto 2
	manager.add_command("db", MigrateCommand)
	# nombres cortos y descriptivos
	@manager.command
	def test():
		import unittest # se debe importar porque usaremos un archivo externo de la carpeta test
		tests = unittest.TestLoader().discover("tests") # buscamos la carpeta test
		unittest.TextTestRunner().run(tests)

	manager.run()