from .app import create_app
from .models import db, BrutalWaitlist

def initialize_database():
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database() 