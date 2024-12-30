from app import app, db
from models import User

def init_database():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Database initialized!")

if __name__ == "__main__":
    init_database() 