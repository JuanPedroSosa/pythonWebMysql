from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from .models import User

def codi_validate(form, field):
	if field.data == "codi" or field.data == "Codi":
		raise validators.ValidationError("username codi no esta permitido")


class LoginForm(Form):
	username = StringField("Usuario:", [validators.length(min=1,max=5, message="no valido"), codi_validate])
	password = PasswordField("Clave:", [validators.Required()])

class RegisterForm(Form):
	username = StringField("Usuario:", [validators.length(min=1,max=5, message="no valido")])
	email = EmailField("Correo:", [validators.length(min=6, max=100), validators.Required(message="email requerido"), validators.Email(message="ingrese correo válido")])
	password = PasswordField("Clave:", [validators.Required(message="la clave es requerida"), validators.EqualTo("confirmpassword", message="la clave no coincide")])
	confirmpassword = PasswordField("Confirmar clave:", [validators.Required(message="la clave es requerida")])
	accept=BooleanField("Acepto terminos y condiciones", [validators.Required()])

	def validate_username(self, username):
		if User.get_by_username(username.data):
			raise validators.ValidationError("Ya se encuentra registrado el usuario")

	# hacer un validador sobreescribiendo el método validate
	def validate(self):
		# ejecutamos la validación del formulario
		if not Form.validate(self):
			return False

		if len(self.password.data) < 3:
			self.password.errors.append("clave muy corta")
			return False
		return True

class TaskForm(Form):
	title = StringField("Título:", [validators.length(min=1,max=50, message="ingrese un título")])
	description = TextAreaField("Descripción:", [validators.Required(message="descripción requerido")], render_kw={"rows": 5})

	#@classmethod
	#def create_element(cls, title, description, user_id):
	#	task = TaskForm(title=title, description=description, user_id=user_id)
	#	db.session.add(task)
	#	db.session.commit()
	#	return task

