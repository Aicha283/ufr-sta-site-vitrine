from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def create_initial_admin():
    # On utilise le contexte de l'application Flask pour accéder à la base de données
    with app.app_context():
        # 1. On vérifie si un admin existe déjà pour éviter les doublons
        admin_existe = Admin.query.filter_by(username="admin").first()
        
        if admin_existe:
            print("L'administrateur 'admin' existe déjà dans la base de données.")
            return

        # 2. On demande à Werkzeug de hacher proprement le mot de passe
        # ATTENTION : Ne stockez JAMAIS un mot de passe en texte clair !
        password_hache = generate_password_hash("AdminSTA2026")

        # 3. On crée l'objet Admin (assurez-vous que vos champs dans models.py s'appellent ainsi)
        nouvel_admin = Admin(
            username="admin",
            password=password_hache
        )

        # 4. On sauvegarde dans ufr_sta.db
        db.session.add(nouvel_admin)
        db.session.commit()
        
        print("======================================================")
        print(" Succès : Compte Administrateur créé avec succès !")
        print(" Identifiant : admin")
        print(" Mot de passe : AdminSTA2026")
        print("======================================================")
        print("⚠️ Pensez à changer ce mot de passe une fois connecté !")

if __name__ == '__main__':
    create_initial_admin()