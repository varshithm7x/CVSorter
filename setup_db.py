from app import app, db
from models import User
from sqlalchemy import inspect

def setup_database():
    with app.app_context():
        try:
            # Check if database exists
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"\nExisting tables: {existing_tables}")
            
            # Create new tables if they don't exist
            if not existing_tables:
                print("\nCreating new tables...")
                db.create_all()
                print("All tables created successfully.")
            else:
                print("\nTables already exist.")
            
            # Verify tables
            for table_name in inspector.get_table_names():
                print(f"\nTable: {table_name}")
                for column in inspector.get_columns(table_name):
                    print(f"- Column: {column['name']} ({column['type']})")

        except Exception as e:
            print(f"Error during database setup: {str(e)}")
            raise e

if __name__ == "__main__":
    setup_database() 