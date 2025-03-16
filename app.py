from flask import Flask
from config import Config
from db.connection import db
from routes.loja_routes import loja_routes

app = Flask(__name__)

# configura do banco e inicializa o banco
app.config.from_object(Config)
db.init_app(app)  # Added app to db

# registra as rots
app.register_blueprint(loja_routes)

if __name__ == '__main__':
    app.run(debug=True)
