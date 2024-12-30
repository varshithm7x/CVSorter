from app import app, db
from models import User

def setup_database():
    with app.app_context():
        # Drop existing tables
        db.drop_all()
        print("Dropped all tables.")
        
        # Create new tables
        db.create_all()
        print("Created all tables.")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"- Column: {column['name']} ({column['type']})")

if __name__ == "__main__":
    setup_database() 