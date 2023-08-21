from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#Clé secrète
app.config['SECRET_KEY'] = 'c07fad13c2056c2db457ce70d1bc41e8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:psql@localhost/manga'
db = SQLAlchemy(app)
from . import routes
