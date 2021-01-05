from decouple import config

class Config:
	SECRET_KEY="adcfvfv5656bvv67b"

class DevelopmentConfig(Config):
	DEBUG = False
	threaded=True
	SQLALCHEMY_DATABASE_URI = "mysql://telcon:super@localhost/cursoPython"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = "juanpedrososa2013@gmail.com"
	MAIL_PASSWORD = config("PASSWORDMAIL")

# separamos la configuración del enterno de desarrollo
class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = "mysql://telcon:super@localhost/CursoPythonTest"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEST = True

# para la password necesitamos ller desde una variable de entorno. Se podría os pero usaremos decouple
# hay que crear una variable de entorno llamada PASSWORD
# tengo que crear esta variable en .bash_profile
# ingresar a google y buscar: permitir el acceso a cuentas desde apps menos seguras
config = {
	"development" : DevelopmentConfig,
	"default" : DevelopmentConfig,
	"test" : TestConfig
}