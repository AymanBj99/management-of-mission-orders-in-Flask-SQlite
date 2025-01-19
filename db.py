from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

# Créez une instance de Flask
app = Flask(__name__)

# Configurations de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'  # Remplacez par votre URI de base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'

# Créez l'instance SQLAlchemy
db = SQLAlchemy()
migrate = Migrate(app, db)

# Initialisez l'application avec SQLAlchemy
db.init_app(app)
