from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, FloatField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class MissionForm(FlaskForm):
    # Champs liés à la mission
    projet = StringField('Nom du Projet', validators=[DataRequired(), Length(max=100)])
    chef_de_projet = StringField('Chef de Projet', validators=[DataRequired(), Length(max=100)])
    chauffeur = StringField('Chauffeur', validators=[DataRequired(), Length(max=100)])
    marque_vehicule = StringField('Marque du Véhicule', validators=[DataRequired(), Length(max=50)])
    matricule_vehicule = StringField('Matricule du Véhicule', validators=[DataRequired(), Length(max=20)])
    designation_travaux = StringField('Désignation des Travaux', validators=[DataRequired(), Length(max=200)])
    site_client = StringField('Site ou Client', validators=[DataRequired(), Length(max=100)])
    ville_depart = StringField('Ville de Départ', validators=[DataRequired(), Length(max=50)])
    ville_arrivee = StringField('Ville d\'Arrivée', validators=[DataRequired(), Length(max=50)])
    date_debut = DateField('Date de Début', validators=[DataRequired()], format='%Y-%m-%d')
    date_fin = DateField('Date de Fin', validators=[DataRequired()], format='%Y-%m-%d')
    recharge_gasoil = FloatField('Recharge Gasoil (L)', validators=[DataRequired()])
    
    # Champs liés au responsable
    responsable_id = SelectField('Responsable', coerce=int, validators=[DataRequired()])
    
    # Nouveau champ pour sélectionner l'équipe accompagnante
    equipe_ids = SelectMultipleField('Équipe Accompagnante', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Enregistrer Mission')
