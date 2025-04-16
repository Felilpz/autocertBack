from flask import Flask
from flask_cors import CORS  # Import the CORS module
from config import Config
from db.connection import db
from routes.loja_routes import loja_routes

app = Flask(__name__)

CORS(app)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(loja_routes)

if __name__ == '__main__':
    app.run(debug=True)