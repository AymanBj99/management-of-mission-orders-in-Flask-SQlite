from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User, Mission
from db import db, app
from admin import insert_admins
from datetime import datetime




# Route de connexion
@app.route('/')
def index():
    if 'username' in session:
        # Récupérer l'utilisateur connecté
        username = session['username']
        user = User.query.filter_by(username=username).first()

        # Vérifier si l'utilisateur est un admin (ici, on compare avec des admins définis manuellement)
        admin_users = ['admin1', 'admin2']  # Liste des utilisateurs admins définis manuellement

        if user and username in admin_users:
            # Si c'est un admin, rediriger vers l'interface admin
            return redirect(url_for('gererMissions'))
        elif user:
            # Si c'est un employé, rediriger vers l'interface employé
            return redirect(url_for('employee'))
        else:
            flash('Utilisateur non trouvé', 'error')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Récupérer l'utilisateur par son nom d'utilisateur
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['username'] = user.username
            flash('Connexion réussie', 'success')
            return redirect(url_for('index'))  # Rediriger vers la page d'accueil après connexion
        else:
            flash('Nom d\'utilisateur ou mot de passe invalide', 'error')
    
    return render_template('login.html')  # Afficher le formulaire de connexion


# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()

        if existing_user is None:
            # Hachage du mot de passe
            password_hash = generate_password_hash(password)
            # Créer un nouvel utilisateur
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie, vous pouvez vous connecter', 'success')
            return redirect(url_for('login'))
        else:
            flash('Le nom d\'utilisateur existe déjà, veuillez en choisir un autre', 'error')

    return render_template('register.html')



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
    missions = Mission.query.all()

    return render_template('missions.html', missions=missions)



#Ajouter une mission
@app.route('/add_mission', methods=['GET', 'POST'])
def addMission():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        titre = request.form['titre']
        destination = request.form['destination']
        idUser = request.form['user_id']
        matricule = request.form['matricule']
        marque = request.form['marque']
        chauffeur = request.form['chauffeur']
        montant_gasoil = float(request.form['montant_gasoil'])
        nom_projet = request.form['nom_projet']
        chef_projet = request.form['chef_projet']
        client = request.form['client']

        # Convert date strings to date objects
        date_depart = datetime.strptime(request.form['date_depart'], '%Y-%m-%d').date()
        date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()

        # Créer la nouvelle mission avec les attributs de transport et de projet intégrés
        new_mission = Mission(
            titre=titre,
            destination=destination,
            user_id=idUser,
            date_depart=date_depart,
            date_retour=date_retour,
            matricule=matricule,
            marque=marque,
            chauffeur=chauffeur,
            montant_gasoil=montant_gasoil,
            nom_projet=nom_projet,
            chef_projet=chef_projet,
            client=client
        )

        db.session.add(new_mission)
        db.session.commit()

        flash('Mission ajoutée avec succès', 'success')
        return redirect(url_for('gererMissions'))

    # Récupérer les utilisateurs pour les afficher dans la liste déroulante
    users = User.query.all()

    return render_template('addMission.html', users=users)

#afficher mission 
@app.route('/mission_details/<int:id>', methods=['GET'])
def mission_details(id):
    # Récupérer la mission avec ses relations
    mission = Mission.query.get_or_404(id)
    return render_template('afficherMission.html', mission=mission)

#Modifier une mission
@app.route('/editMission/<int:id>', methods=['GET', 'POST'])
def edit_mission(id):
    mission= Mission.query.get_or_404(id)
    users = User.query.all()
    if request.method == 'POST':
        mission.titre = request.form['titre']
        mission.destination = request.form['destination']
        mission.user_id = request.form['user_id']
        mission.matricule = request.form['matricule']
        mission.marque = request.form['marque']
        mission.chauffeur = request.form['chauffeur']
        mission.montant_gasoil = float(request.form['montant_gasoil'])
        mission.nom_projet = request.form['nom_projet']
        mission.chef_projet = request.form['chef_projet']
        mission.client = request.form['client']
        mission.date_depart = datetime.strptime(request.form['date_depart'], '%Y-%m-%d').date()
        mission.date_retour = datetime.strptime(request.form['date_retour'], '%Y-%m-%d').date()


        # Mise à jour des autres champs nécessaires
        db.session.commit()
        flash('Mission mis à jour avec succès', 'success')
        return redirect(url_for('gererMissions'))
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

#Gerer les utilisateurs
@app.route('/gerer_users', methods=['GET'])
def gererUsers():
    # Récupérer les personnels existants pour les afficher
    users = User.query.all()

    return render_template('users.html', users=users)



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






#Executer
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        insert_admins()
    app.run(debug=True)



