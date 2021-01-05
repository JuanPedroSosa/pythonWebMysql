from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
	usuario = "Pedro"
	ispremium = True
	return render_template("index.html", name=usuario, ispremium=ispremium)

if __name__ == '__main__':
	app.run(debug=True)