from app import app
from models import db, Actualite

with app.app_context():
    Actualite.query.delete()
    db.session.commit()
    print("✅ Actualités supprimées")