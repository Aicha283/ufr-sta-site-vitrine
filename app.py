from flask import Flask, render_template,request,redirect,session,flash,url_for
from models import db, Departement, Formation, Actualite, Activite, Enseignant, Album,Admin,PhotoActivite
from datetime import datetime
import functools
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ufr_sta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ufr-sta-secret-key'

db.init_app(app)

with app.app_context():
    db.create_all()
# ===== DÉCORATEUR PROTECTION ADMIN =====
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    actualites = Actualite.query.order_by(Actualite.date.desc()).limit(3).all()
    return render_template('index.html', actualites=actualites)

@app.route('/departements')
def departements():
    departements = Departement.query.all()
    return render_template('departements.html', departements=departements)

@app.route('/formations')
def formations():
    formations = Formation.query.all()
    return render_template('formations.html', formations=formations)

@app.route('/actualites')
def actualites():
    actualites = Actualite.query.order_by(Actualite.date.desc()).all()
    return render_template('actualites.html', actualites=actualites)

@app.route('/activites')
def activites():
    activites = Activite.query.order_by(Activite.date.desc()).all()
    return render_template('activités.html', activites=activites)

@app.route('/enseignants')
def enseignants():
    enseignants = Enseignant.query.all()
    return render_template('enseignants.html', enseignants=enseignants)

@app.route('/galerie')
def galerie():
    albums = Album.query.all()
    return render_template('galerie.html', albums=albums)

@app.route('/contact')
def contact():
    return render_template('contact.html')


# Configuration du dossier de téléchargement des images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer automatiquement le dossier static/uploads s'il n'existe pas encore
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# ===== ROUTES ADMIN =====
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    erreur = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Identifiants incorrects","error")
    return render_template('admin/login.html')        
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash("Vous avez été déconnecté avec succés.","info")
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    toutes_les_actualites = Actualite.query.order_by(Actualite.date.desc()).all()
    toutes_les_activites = Activite.query.order_by(Activite.date.desc()).all()
    tous_les_albums = Album.query.order_by(Album.date.desc()).all() # <-- AJOUT ICI
    
    # On passe tout au template
    return render_template(
        'admin/dashboard.html', 
        actualites=toutes_les_actualites, 
        activites=toutes_les_activites,
        albums=tous_les_albums # <-- AJOUT ICI
    )

# . GESTION DU FORMULAIRE D'ACTUALITÉ
# ==========================================
@app.route('/admin/actualites/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_actualite():
    # SI L'ADMIN VALIDE LE FORMULAIRE (Méthode POST)
    if request.method == 'POST':
        # On extrait les données saisies grâce à l'attribut 'name' des inputs HTML
        titre_saisi = request.form['titre']
        description_saisie = request.form['description']
        date1=datetime.now().date()
        #  Gestion de la photo
        nom_photo = None # Par défaut, pas de photo si l'admin n'en choisit pas
        if 'photo' in request.files:
            fichier = request.files['photo']
            # On vérifie que l'utilisateur a bien sélectionné un fichier
            if fichier and fichier.filename != '':
                # secure_filename nettoie le nom du fichier (ex: "mon image.png" -> "mon_image.png")
                nom_photo = secure_filename(fichier.filename)
                # Sauvegarde physique de l'image dans static/uploads/
                fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_photo))

        
        # On crée la ligne à insérer dans la base de données
        nouvelle_actu = Actualite(titre=titre_saisi, date=date1, description=description_saisie, photo=nom_photo)
        
        # On sauvegarde le tout dans ufr_sta.db avec SQLAlchemy
        db.session.add(nouvelle_actu)
        db.session.commit()
        
        # On envoie une notification de confirmation
        flash("L'actualité a été publiée sur le site avec succès !", "success")
        
        # On redirige l'administrateur vers le tableau de bord
        return redirect(url_for('admin_dashboard'))
        
    # SI L'ADMIN VEUT JUSTE OUVRIR LA PAGE (Méthode GET)
    return render_template('admin/form_actualité.html')
@app.route('/admin/actualites/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_actualite(id):
    actu = Actualite.query.get_or_404(id)
    if request.method == 'POST':
        actu.titre = request.form['titre']
        actu.description = request.form['description']
        
        # Si l'admin télécharge une nouvelle photo
        if 'photo' in request.files:
            fichier = request.files['photo']
            if fichier and fichier.filename != '':
                nom_photo = secure_filename(fichier.filename)
                fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_photo))
                actu.photo = nom_photo # Met à jour le nom de l'image
                
        db.session.commit()
        flash("L'actualité a été modifiée !", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/form_actualite.html', actu=actu)


@app.route('/admin/actualites/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer_actualite(id):
    actu = Actualite.query.get_or_404(id)
    db.session.delete(actu)
    db.session.commit()
    flash("L'actualité a été supprimée.", "danger")
    return redirect(url_for('admin_dashboard'))
@app.route('/activites')
def afficher_le_journal_des_activites():
    # Va chercher toutes les activités dans ufr_sta.db, de la plus récente à la plus ancienne
    toutes_les_activites = Activite.query.order_by(Activite.date.desc()).all()
    
    # Envoie la liste des activités au template public (activites.html)
    return render_template('activités.html', activites_a_afficher=toutes_les_activites)


# =======================================================
#  ESPACE ADMIN : Ajouter une Activité depuis le Dashboard
# =======================================================
@app.route('/admin/activites/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_activite():
    # SI L'ADMIN A REMPLI ET ENVOYÉ LE FORMULAIRE (Méthode POST)
    if request.method == 'POST':
        # 1. Extraction des données tapées dans le formulaire HTML
        titre_saisi = request.form['titre']
        lieu_saisi = request.form['lieu']
        organisateur_saisi = request.form['organisateur']
        description_saisie = request.form['description']
        date_saisie_str = request.form['date']  # Reçoit la date au format texte "YYYY-MM-DD"
        
        # 2. Conversion de la date texte en un objet Date lisible par SQLAlchemy
        date_objet = datetime.strptime(date_saisie_str, '%Y-%m-%d').date()
        
        # 3. Création de l'enregistrement en respectant votre models.py
        nouvelle_activite = Activite(
            titre=titre_saisi,
            lieu=lieu_saisi,
            organisateur=organisateur_saisi,
            description=description_saisie,
            date=date_objet  # Remplit le champ db.Date (nullable=False)
        )
        
        db.session.add(nouvelle_activite)
        db.session.flush()

        # . Gestion des images multiples
        if 'photos[]' in request.files:
            fichiers = request.files.getlist('photos') # getlist permet de récupérer TOUS les fichiers
            for fichier in fichiers:
                if fichier and fichier.filename != '':
                    # Sécurisation du nom de fichier
                    nom_fichier = secure_filename(fichier.filename)
                    # Sauvegarde physique
                    fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
                    
                    # Liaison en base de données
                    nouvelle_photo = PhotoActivite(nom_fichier=nom_fichier, activite_id=nouvelle_activite.id)
                    db.session.add(nouvelle_photo)
        
        # Sauvegarde finale en BDD
        db.session.commit()
        # 5. Message flash et redirection vers le menu admin
        flash("L'activité a été ajoutée au journal avec succès !", "success")
        return redirect(url_for('admin_dashboard'))
        
    # SI L'ADMIN CLIQUE JUSTE SUR LE BOUTON POUR OUVRIR LA PAGE (Méthode GET)
    return render_template('admin/form_activité.html')
@app.route('/admin/activites/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_activite(id):
    activite = Activite.query.get_or_404(id)
    if request.method == 'POST':
        activite.titre = request.form['titre']
        activite.lieu = request.form['lieu']
        activite.organisateur = request.form.get('organisateur')
        activite.description = request.form['description']
        
        date_saisie_str = request.form['date']
        activite.date = datetime.strptime(date_saisie_str, '%Y-%m-%d').date()
        
        # Ajout de photos supplémentaires à la galerie si souhaité
        if 'photos[]' in request.files:
            fichiers = request.files.getlist('photos[]')
            for fichier in fichiers:
                if fichier and fichier.filename != '':
                    nom_fichier = secure_filename(fichier.filename)
                    fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
                    
                    nouvelle_photo = PhotoActivite(nom_fichier=nom_fichier, activite_id=activite.id)
                    db.session.add(nouvelle_photo)
                    
        db.session.commit()
        flash("L'activité a bien été modifiée !", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/form_activite.html', activite=activite)


@app.route('/admin/activites/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer_activite(id):
    activite = Activite.query.get_or_404(id)
    # Grâce au cascade="all, delete-orphan" dans models.py, 
    # les lignes associées dans PhotoActivite seront nettoyées automatiquement.
    db.session.delete(activite)
    db.session.commit()
    flash("L'activité a été supprimée.", "danger")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/galerie/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_album():
    if request.method == 'POST':
        # 1. Récupération des champs textes du formulaire
        titre_saisi = request.form.get('titre')
        description_saisie = request.form.get('description')
        date_saisie_str = request.form.get('date')
        
        # Validation rapide
        if not titre_saisi or not date_saisie_str:
            flash("Le titre et la date sont obligatoires !", "danger")
            return redirect(request.url)
            
        try:
            # Conversion de la chaîne 'AAAA-MM-JJ' en objet date Python
            date_objet = datetime.strptime(date_saisie_str, '%Y-%m-%d').date()
            
            # 2. Création et enregistrement de l'album en BDD
            nouvel_album = Album(
                titre=titre_saisi,
                description=description_saisie,
                date=date_objet
            )
            db.session.add(nouvel_album)
            db.session.flush()  # Crucial : génère l'ID de l'album avant le commit pour lier les photos

            # 3. Gestion des fichiers / photos multiples
            if 'photos[]' in request.files:
                fichiers = request.files.getlist('photos[]')
                
                for fichier in fichiers:
                    if fichier and fichier.filename != '':
                        # Sécurisation du nom de l'image
                        nom_fichier = secure_filename(fichier.filename)
                        
                        # Sauvegarde physique du fichier dans static/uploads/
                        chemin_sauvegarde = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier)
                        fichier.save(chemin_sauvegarde)
                        
                        # Création de la ligne PhotoActivite liée à notre album
                        nouvelle_photo = PhotoActivite(
                            nom_fichier=nom_fichier, 
                            album_id=nouvel_album.id
                        )
                        db.session.add(nouvelle_photo)
            
            # Validation finale dans la base de données
            db.session.commit()
            flash("L'album et ses photos ont été ajoutés avec succès !", "success")
            return redirect(url_for('admin_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Une erreur est survenue lors de l'ajout : {str(e)}", "danger")
            return redirect(request.url)

    # Si c'est une requête GET, on affiche simplement le formulaire
    return render_template('admin/form_galerie.html')
@app.route('/admin/galerie/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_album(id):
    album = Album.query.get_or_404(id)
    
    if request.method == 'POST':
        #  Mise à jour des infos basiques
        album.titre = request.form['titre']
        album.description = request.form.get('description')
        date_saisie_str = request.form['date']
        album.date = datetime.strptime(date_saisie_str, '%Y-%m-%d').date()
        
        #  Ajout de nouvelles photos si l'admin en a sélectionné
        if 'photos[]' in request.files:
            fichiers = request.files.getlist('photos[]')
            for fichier in fichiers:
                if fichier and fichier.filename != '':
                    nom_fichier = secure_filename(fichier.filename)
                    fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
                    
                    nouvelle_photo = PhotoActivite(nom_fichier=nom_fichier, album_id=album.id)
                    db.session.add(nouvelle_photo)
                    
        db.session.commit()
        flash("L'album a été mis à jour avec succès !", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/form_modifier_album.html', album=album)


@app.route('/admin/galerie/supprimer-photo/<int:photo_id>', methods=['POST'])
@login_required
def supprimer_photo_album(photo_id):
    photo = PhotoActivite.query.get_or_404(photo_id)
    id_album = photo.album_id # On garde l'ID pour rediriger au même endroit
    
    # Suppression logique en BDD
    db.session.delete(photo)
    db.session.commit()
    
    flash("La photo a été retirée de l'album.", "success")
    return redirect(url_for('modifier_album', id=id_album))
@app.route('/admin/galerie/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer_album(id):
    album = Album.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    flash("L'album et toutes ses photos ont été supprimés.", "danger")
    return redirect(url_for('admin_dashboard'))
if __name__ == '__main__':
    app.run(debug=True)