from app import app
from models import db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    # Supprimer ancien admin
    Admin.query.delete()
    db.session.commit()
    
    # Créer nouvel admin
    admin = Admin(
        username="admin",
        password=generate_password_hash("admin123")
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin créé avec succès !")