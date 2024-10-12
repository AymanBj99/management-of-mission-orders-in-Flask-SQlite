from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from modele import User
from db import db, app
from admin import insert_admins




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
            return redirect(url_for('admin'))
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
    session.pop('username', None)
    flash('Vous êtes déconnecté', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créez toutes les tables si elles n'existent pas
        insert_admins()  # Insérer les administrateurs manuellement  
    app.run(debug=True)
