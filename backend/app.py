from flask import Flask
from flask_cors import CORS
from routes import define_routes

app = Flask(__name__)
define_routes(app)
CORS(app)

if __name__ == '__main__':
	app.run()
