from app import create_app, db
from app.models.user_model import user as User
from flask import current_app


def create_initial_users():
    def _create():
        seeds = [
            {
                "nombre": "Admin",
                "apellidos": "Default",
                "correo": "admin@local.test",
                "password": "Admin1234",
                "rol": "Administrador",
            },
            {
                "nombre": "Profesor",
                "apellidos": "Default",
                "correo": "profesor@local.test",
                "password": "Prof1234",
                "rol": "Profesor",
            },
            {
                "nombre": "Alumno",
                "apellidos": "Default",
                "correo": "alumno@local.test",
                "password": "Alumno1234",
                "rol": "Alumno",
            },
        ]

        created = 0
        for s in seeds:
            if User.query.filter_by(correo=s["correo"]).first():
                print(f"Saltando {s['correo']}: ya existe")
                continue

            u = User(
                nombre=s["nombre"],
                apellidos=s["apellidos"],
                correo=s["correo"],
                rol=s["rol"],
            )

            u.set_password(s["password"])
            db.session.add(u)
            created += 1

        if created > 0:
            db.session.commit()
            print(f"* => {created} usuarios creados exitosamente")
        else:
            print("* => No se crearon usuarios (ya existían).")

        return created

    
    try:
        
        _ = current_app.name
        return _create()
    except RuntimeError:
        app = create_app()
        with app.app_context():
            return _create()


if __name__ == "__main__":
    create_initial_users()
