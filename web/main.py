import toga

def on_press(wigget):
	print("toga")

def new_button():
	button = toga.Button("clic", on_press=on_press)
	button.style.padding = 20
	button.style.font_size = 20
	return button

def build(app):
	box = toga.Box()
	button1 = new_button()
	print("agregar")
	box.add(button1)

	return box

def main():
	app = toga.App("Hola mundo", "com.codigofacilito.toga", startup=build)
	return app

if __name__ == "__main__":
	app = main()
	app.main_loop()
