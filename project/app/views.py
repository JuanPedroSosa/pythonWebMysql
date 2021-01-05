from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Task
from .consts import *
from .email import welcome_mail
from . import login_manager

# blueprint grandes proyectos modilable
page = Blueprint("page", __name__)

# UserMixin buscará a través de esta función el usuario para saber si pertenece a la sesión
@login_manager.user_loader
def load_user(id):
	return User.get_by_id(id)
#por buenas practicas retornamos el error también 404
@page.app_errorhandler(404)
def page_not_found(error):
	return render_template("errors/404.html"), 404

@page.route("/")
def index():
	return render_template("index.html", title="index")

@page.route("/logout")
def logout():
	logout_user()
	flash("Cerraste sesión")
	return redirect(url_for(".login")) # redirigir función login, el punto hace referencia a page

@page.route("/login", methods=["GET", "POST"])
def login():

	if current_user.is_authenticated:
		return redirect(url_for(".task"))

	form = LoginForm(request.form)

	if request.method == "POST" and form.validate():
		print(form.username.data)
		user = User.get_by_username(form.username.data)
		if user and user.verify_password(form.password.data):
			login_user(user)
			flash("usuario autenticado correctamente")
		else:
			flash("usuario o clave inválidos", "error")

	return render_template("auth/login.html", title="login", form=form, active="login")

@page.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for(".task"))

	form = RegisterForm(request.form)
	#print(request.method)

	if request.method == "POST":
		print("vamos a validar usuario")
		if form.validate():
			user = User.create_element(form.username.data, form.password.data, form.email.data)
			print("usuario registrado")
			flash("Usuario registrado correctamente")
			login_user(user)
			welcome_mail(user)
		else:
			print("usuario no registrado")
			flash("Usuario no registrado")

	return render_template("auth/register.html", title="register", form=form, active="register")

@page.route("/task")
@page.route("/task/<int:page>")
@login_required
def task(page=1, per_page=2):
	#tasks = current_user.task # estaba sin paginar
	pagination = current_user.task.paginate(page, per_page=per_page)
	tasks = pagination.items

	return render_template("task/list.html", title="Tareas", tasks=tasks, pagination=pagination, page=page, active="task")

@page.route("/task/new", methods=["GET", "POST"])
@login_required
def new_task():
	form = TaskForm(request.form)

	if request.method == "POST":
		if form.validate():
			task = Task.create_element(form.title.data, form.description.data, current_user.id)

			if task:
				flash("Tarea creada correctamente")
	return render_template("task/new.html", title="Nueva tarea", form=form, active="new_task")

@page.route("/task/show/<int:task_id>")
@login_required
def get_task(task_id):
	task = Task.query.get_or_404(task_id)

	return render_template("task/show.html", title="Tareas", task=task)

@page.route("/task/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
	task = Task.query.get_or_404(task_id)
	if task.user_id != current_user.id:
		abort(404)

	form = TaskForm(request.form, obj=task)

	if request.method == "POST" and form.validate():
		task = Task.update_element(task.id, form.title.data, form.description.data)
		if task:
			flash("Tarea actualizad")

	return render_template("task/edit.html", title="editar tarea", form=form)

@page.route("/task/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)

	if task.user_id != current_user.id:
		abort(404)

	if Task.delete_element(task.id):
		flash("Tarea eliminada exi")

	return redirect(url_for(".task"))

