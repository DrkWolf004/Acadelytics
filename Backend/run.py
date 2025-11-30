from app import create_app, db
import os

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created.")

    
    try:
        from app.initialSetup import create_initial_users
        created = create_initial_users()
        print(f"initialSetup: usuarios creados = {created}")
    except Exception as e:
        print("Error ejecutando initialSetup:", e)

if __name__ == '__main__':
    app.run(debug=True)
