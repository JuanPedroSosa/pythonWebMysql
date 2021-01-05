from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from . import mail, app
# enviamos el correo desde el contexto de la app
# si no se envía a través del contexto el correo no puede ser enviado de forma asíncrona
def send_async_mail(message):
	with app.app_context():
		mail.send(message)

def welcome_mail(user):
	message = Message("Bienvenido al proyecto",
	sender=current_app.config["MAIL_USERNAME"],
	recipients=[user.email])
# el cuerpo del correo se utilizan etiquetas html
	message.html = render_template("email/welcome.html", user=user)
	thread = Thread(target=send_async_mail, args=[message])
	thread.start()
