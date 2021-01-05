import toga
import requests
import threading

from consts import *

class PokeDex(toga.App):
	def __init__(self, title, id):
		toga.App.__init__(self, title, id)
		self.title = title
		self.width = WITDH
		self.height = HEIGHT
		self.heading = ["name"]
		self.data = list()
		self.create_element()
		self.offset = 0
		#sincronico
		#self.load_data()
		#asíncronico
		self.load_async_data()
		self.validate_previous_command()

	def startup(self):
		self.main_window = toga.MainWindow("main", title=self.title, size=(self.width,self.height))
		box = toga.Box()
		#box.add(self.table)
		box.add(self.image_view)

		split = toga.SplitContainer()
		split.content = [self.table, box]

		#self.main_window.content = box
		self.main_window.content = split
		self.main_window.toolbar.add(self.previous_command, self.next_command)
		self.main_window.show()

	def create_element(self):
		self.create_table()
		self.create_toolbar()
		self.create_image(METAPOD)

	def create_table(self):
		self.table = toga.Table(self.heading, data=self.data, on_select=self.select_item)

	def create_toolbar(self):
		self.create_next_command()
		self.create_previous_command()

	def create_next_command(self):
		self.next_command = toga.Command(self.next, label="NEXT", tooltip="", icon=BULBASUAR)

	def create_previous_command(self):
		self.previous_command = toga.Command(self.previous, label="PREVIOUS", tooltip="", icon=METAPOD)

	def create_image(self, path):
		image = toga.Image(path)
		self.image_view = toga.ImageView(image)

	# CALLBACKS
	def select_item(self, widget,row):
		if row:
			print(row.name)

	def next(self, widget):
		self.offset *= 1
		self.handler_command(widget)
		#self.load_async_data()
		#self.validate_previous_command()

	def previous(self, widget):
		self.offset -= 1
		self.handler_command(widget)
		#self.load_async_data()
		#self.validate_previous_command()

	def handler_command(self, widget):
		widget.enabled = False
		self.load_async_data()
		widget.enabled = True
		self.validate_previous_command()

	def validate_previous_command(self):
		self.previous_command.enabled = not self.offset == 0

	def load_async_data(self):
		self.data.clear()
		self.table.data = self.data
		thread = threading.Thread(target=self.load_data)
		thread.start()
		# evitar que el threas opere sobre la tabla
		thread.join()
		self.table.data = self.data

	def load_data(self):
		#self.data.clear()
		#path = "https://pokeapi.co/api/v2/pokemon-form?offset=0&limit=20"
		path = "https://pokeapi.co/api/v2/pokemon-form?offset={}&limit=20".format(self.offset)

		response = requests.get(path)

		if response:
			result = response.json()

			for pokemon in result["results"]:
				name = pokemon["name"]
				self.data.append(name)

		#self.table.data = self.data


if __name__ == "__main__":
	print("1")
	podex = PokeDex("PokeDex", "com.codigofacilito.poke")
	print("2")
	podex.main_loop()