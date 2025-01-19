from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User, Mission, MissionUser
from db import db, app
from admin import insert_admins
from datetime import datetime
from forms import MissionForm




# Route de connexion
@app.route('/')
def index():
    if 'email' in session:
        # Récupérer l'utilisateur connecté
        email = session['email']
        user = User.query.filter_by(email=email).first()

        # Vérifier si l'utilisateur est un admin (en comparant avec des e-mails d'admins prédéfinis)
        admin_emails = ['admin1@example.com', 'admin2@example.com']  # Liste des e-mails admins définis manuellement

        if user and email in admin_emails:
            # Si c'est un admin, rediriger vers l'interface admin
            return redirect(url_for('gererMissions'))
        elif user:
            # Si c'est un employé, rediriger vers l'interface employé
            return redirect(url_for('employe'))
        else:
            flash('Utilisateur non trouvé', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si non connecté


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  # Récupérer l'e-mail depuis le formulaire
        password = request.form['password']  # Récupérer le mot de passe depuis le formulaire

        # Rechercher l'utilisateur par son e-mail
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['email'] = user.email  # Stocker l'e-mail dans la session
            
            flash('Connexion réussie', 'success')
            return redirect(url_for('index'))  # Rediriger vers la route index pour gérer la redirection
        else:
            flash('E-mail ou mot de passe invalide', 'error')

    return render_template('login.html')  # Rendre le formulaire de connexion





# Route de déconnexion
@app.route('/logout')
def logout():
    # Supprime les données de session
    session.pop('user_id', None)
    flash("Vous avez été déconnecté avec succès.", "info")
    return redirect(url_for('login'))




#Partie Mission 

#Gerer la mission
@app.route('/gerer_missions', methods=['GET'])
def gererMissions():
    # Récupérer les missions existantes pour les afficher
    missions = Mission.query.all()  # Récupérer toutes les missions depuis la base de données
    return render_template('missions.html', missions=missions)

#Gerer les utilisateurs
@app.route('/gerer_users', methods=['GET'])
def gererUsers():
    # Récupérer les personnels existants pour les afficher
    users = User.query.all()

    return render_template('users.html', users=users)

#Ajouter une mission
@app.route('/addmission', methods=['GET', 'POST'])
def add_mission():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        projet = request.form['projet']
        chef_de_projet = request.form['chef_de_projet']
        chauffeur = request.form['chauffeur']
        marque_vehicule = request.form['marque_vehicule']
        matricule_vehicule = request.form['matricule_vehicule']
        designation_travaux = request.form['designation_travaux']
        site_client = request.form['site_client']
        ville_depart = request.form['ville_depart']
        ville_arrivee = request.form['ville_arrivee']
        date_debut = request.form['date_debut']
        date_fin = request.form['date_fin']
        recharge_gasoil = float(request.form['recharge_gasoil'])
        responsable_id = int(request.form['responsable_id'])
        user_ids = request.form.getlist('users')

        # Créer une nouvelle mission
        nouvelle_mission = Mission(
            projet=projet,
            chef_de_projet=chef_de_projet,
            chauffeur=chauffeur,
            marque_vehicule=marque_vehicule,
            matricule_vehicule=matricule_vehicule,
            designation_travaux=designation_travaux,
            site_client=site_client,
            ville_depart=ville_depart,
            ville_arrivee=ville_arrivee,
            date_debut=datetime.strptime(date_debut, '%Y-%m-%d').date(),
            date_fin=datetime.strptime(date_fin, '%Y-%m-%d').date(),
            recharge_gasoil=recharge_gasoil,
            responsable_id=responsable_id
        )
        db.session.add(nouvelle_mission)
        db.session.commit()

        # Associer les utilisateurs sélectionnés
        for user_id in user_ids:
            relation = MissionUser(mission_id=nouvelle_mission.id, user_id=int(user_id))
            db.session.add(relation)

        db.session.commit()
        flash('Mission ajoutée avec succès!', 'success')
        return redirect(url_for('gererMissions'))

    # Envoyer la liste des utilisateurs à la page
    users = User.query.filter(User.role != 'admin').all()
    return render_template('addMission.html', users=users)

#afficher mission 
@app.route('/mission_details/<int:id>', methods=['GET'])
def mission_details(id):
    # Récupérer la mission avec ses relations
    mission = Mission.query.get_or_404(id)
    return render_template('afficherMission.html', mission=mission)

#Modifier une mission
@app.route('/mission/edit/<int:id>', methods=['GET', 'POST'])
def edit_mission(id):
    mission = Mission.query.get_or_404(id)
    users = User.query.all()

    if request.method == 'POST':
        try:
            # Conversion des dates en objets date
            date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d').date()
            date_fin = datetime.strptime(request.form['date_fin'], '%Y-%m-%d').date()

            # Mise à jour des champs
            mission.projet = request.form['projet']
            mission.chef_de_projet = request.form['chef_de_projet']
            mission.chauffeur = request.form['chauffeur']
            mission.marque_vehicule = request.form['marque_vehicule']
            mission.matricule_vehicule = request.form['matricule_vehicule']
            mission.designation_travaux = request.form['designation_travaux']
            mission.site_client = request.form['site_client']
            mission.ville_depart = request.form['ville_depart']
            mission.ville_arrivee = request.form['ville_arrivee']
            mission.date_debut = date_debut  # Conversion appliquée
            mission.date_fin = date_fin      # Conversion appliquée
            mission.recharge_gasoil = float(request.form['recharge_gasoil'])
            mission.responsable_id = int(request.form['responsable_id'])
            mission.user_ids = request.form.getlist('users')

            # Sauvegarde des modifications
            db.session.commit()
            flash(('success', 'Mission mise à jour avec succès !'))
            return redirect(url_for('gererMissions'))

        except Exception as e:
            # Gestion des erreurs
            flash(('danger', f"Erreur lors de la mise à jour : {str(e)}"))
            db.session.rollback()

    return render_template('editMission.html', mission=mission, users=users)


#Supprimer mission
@app.route('/delete_mission/<int:id>', methods=['POST'])
def delete_mission(id):
    # Récupérer la mission par son ID
    mission = Mission.query.get_or_404(id)

    # Supprimer la mission
    db.session.delete(mission)
    db.session.commit()

    flash("Mission supprimée avec succès", "success")
    return redirect(url_for('gererMissions'))

#Etat de la mission
@app.route('/update_etat/<int:mission_id>', methods=['POST'])
def update_etat(mission_id):
    # Récupérer la mission par son ID
    mission = Mission.query.get_or_404(mission_id)

    # Mettre à jour l'état
    mission.etat = "Validée"
    db.session.commit()

    flash("Mission validée avec succès", "success")
    return redirect(url_for('gererMissions'))

#Partie User





#Ajouter un utilisateur
@app.route('/add_user', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        nom = request.form['nom']
        prenom = request.form['prenom']
        fonction = request.form['fonction']
        direction = request.form['direction']
        cin = request.form['cin']
        tel = request.form['tel']
        rib = request.form['rib']

        # Vérification de l'unicité pour email et cin
        existing_user = User.query.filter((User.email == email) | (User.cin == cin)).first()
        if existing_user:
            flash('Un utilisateur avec cet email ou CIN existe déjà.', 'danger')
            return redirect(url_for('addUser'))

        # Créer la nouvelle mission
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            nom=nom,
            prenom=prenom,
            fonction=fonction,
            direction=direction,
            cin=cin,
            tel=tel,
            rib=rib
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Personnel ajouté avec succès', 'success')
            return redirect(url_for('gererUsers'))
        except Exception as e:
            db.session.rollback()  # Annuler la transaction en cas d'erreur
            flash(f'Erreur lors de l\'ajout de l\'utilisateur : {str(e)}', 'danger')

    users = User.query.all()
    return render_template('addUser.html', users=users)



#Modifier un utilisateur
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        user.nom = request.form['nom']
        user.prenom = request.form['prenom']
        user.fonction = request.form['fonction']
        user.direction = request.form['direction']
        user.cin = request.form['cin']
        user.tel = request.form['tel']
        user.rib = request.form['rib']

        # Mise à jour des autres champs nécessaires
        db.session.commit()
        flash('Utilisateur mis à jour avec succès', 'success')
        return redirect(url_for('gererUsers'))
    return render_template('editUser.html', user=user)




#Supprimer un utilisateur
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès', 'success')
    return redirect(url_for('gererUsers'))


#Page Employe
@app.route('/employe')
def employe():
    if 'email' in session:
        # Récupérer l'utilisateur connecté par son email
        email = session['email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Rendre une page avec des données spécifiques à l'employé
            return render_template(
                'employe.html',
                user=user  # Envoyer les informations de l'utilisateur à la page
            )
        else:
            flash('Utilisateur introuvable.', 'error')
            return redirect(url_for('login'))
    else:
        flash('Veuillez vous connecter pour accéder à cette page.', 'error')
        return redirect(url_for('login'))


@app.route('/mes_missions')
@login_required
def mes_missions():
    # Filtrer les missions en fonction de l'utilisateur connecté
    missions = Mission.query.filter_by(responsable_id=current_user.idUser).all()
    return render_template('MissionsEmploye.html', missions=missions)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        insert_admins()     
    app.run(debug=True)




