from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class MissionForm(FlaskForm):
    responsable_id = SelectField('Responsable', coerce=int, validators=[DataRequired()])
    projet = StringField('Projet', validators=[DataRequired()])
    chef_de_projet = StringField('Chef de projet', validators=[DataRequired()])
    chauffeur = StringField('Chauffeur', validators=[DataRequired()])
    marque_vehicule = StringField('Marque de véhicule', validators=[DataRequired()])
    matricule_vehicule = StringField('Matricule de véhicule', validators=[DataRequired()])
    designation_travaux = StringField('Désignation des travaux', validators=[DataRequired()])
    site_client = StringField('Site/Client', validators=[DataRequired()])
    ville_depart = StringField('Ville de départ', validators=[DataRequired()])
    ville_arrivee = StringField('Ville d\'arrivée', validators=[DataRequired()])
    date_debut = DateField('Date de début', validators=[DataRequired()])
    date_fin = DateField('Date de fin', validators=[DataRequired()])
    recharge_gasoil = FloatField('Recharge gasoil', default=0.0)
    equipe_ids = SelectMultipleField('Membres de l\'équipe', coerce=int)  # Multisélection
    submit = SubmitField('Enregistrer')
