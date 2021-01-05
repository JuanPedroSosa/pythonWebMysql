from flask import Flask

from flask_mail import Mail
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

# instancias
app = Flask(__name__)
bootstrap = Bootstrap()
csrf = CSRFProtect()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
# se coloca . porque se importa desde un archivo
from .views import page
from .models import User, Task

def create_app(config):
	app.config.from_object(config)
	csrf.init_app(app)

	# entorno de prueba no llama a bootstrap para no tener conflictos
	if not app.config.get("TEST", False):
		bootstrap.init_app(app)

	# esto se hizo para migration
	app.app_context().push()

	login_manager.init_app(app)
	login_manager.login_view = ".login" # redirigir al usuario cuando NO inició sesión
	login_manager.login_message = "Es necesario iniciar sesión"
	mail.init_app(app)
	app.register_blueprint(page)


	with app.app_context():
		db.init_app(app)
		db.create_all() # crea todas las tablas

	return app