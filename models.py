import os
from . import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired


class Vue_manga_categorie(db.Model):
    id_manga = db.Column(db.Integer, primary_key=True)
    nom_manga = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Float(10), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    nom_categorie = db.Column(db.String(30), nullable=False)
    id_categorie = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.id_manga}:{self.nom_manga}:{self.description}:{self.prix}:{self.image}:{self.nom_categorie}:{self.id_categorie}'


class manga(db.Model):
    id_manga = db.Column(db.Integer, primary_key=True)
    nom_manga = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    prix = db.Column(db.Float(10), nullable=False)
    id_categorie = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f'{self.id_manga} : {self.nom_manga} : {self.description} : {self.prix} : {self.id_categorie} : {self.image}'


class mangaForm(FlaskForm):
    # id_manga = StringField('ID du manga')
    nom_manga = StringField('Nom du Manga', validators=[DataRequired()])
    description = TextAreaField('Description')
    prix = DecimalField('Prix du Manga', validators=[DataRequired()])
    id_categorie = SelectField('Catégorie du manga', choices=[(2, 'Shonen'), (3, 'Shojo'), (4, 'Seinen')])
    image = StringField('Image du Manga?(Si non laissez comme ça)', default='image-non-disponible.jpg')
    submit = SubmitField('Ajouter')


class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"Admin(id_admin={self.id_admin}, login={self.login})"
