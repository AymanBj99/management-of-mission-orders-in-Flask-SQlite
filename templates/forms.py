from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class PersonnelForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    mat = StringField('Matricule', validators=[DataRequired()])
    fonction = StringField('Fonction', validators=[DataRequired()])
    direction = StringField('Direction', validators=[DataRequired()])
    cin = StringField('CIN', validators=[DataRequired()])
    tel = StringField('N° Tel', validators=[DataRequired()])
    rib = StringField('RIB', validators=[DataRequired()])
    submit = SubmitField('Ajouter Personnel')

class VoitureForm(FlaskForm):
    matricule = StringField('Matricule', validators=[DataRequired()])
    marque = StringField('Marque', validators=[DataRequired()])
    chauffeur = StringField('Chauffeur', validators=[DataRequired()])
    montant_gasoil = FloatField('Montant de Gasoil', validators=[DataRequired()])
    submit = SubmitField('Ajouter Voiture')

class ProjetForm(FlaskForm):
    nom = StringField('Nom du Projet', validators=[DataRequired()])
    chef_projet = StringField('Chef de Projet', validators=[DataRequired()])
    client = StringField('Client', validators=[DataRequired()])
    submit = SubmitField('Ajouter Projet')

class MissionForm(FlaskForm):
    titre = StringField('Titre de la Mission', validators=[DataRequired()])
    destination = StringField('Destination', validators=[DataRequired()])
    personnel_id = SelectField('Personnel', coerce=int, validators=[DataRequired()])
    voiture_id = SelectField('Voiture', coerce=int, validators=[DataRequired()])
    projet_id = SelectField('Projet', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Ajouter Mission')
