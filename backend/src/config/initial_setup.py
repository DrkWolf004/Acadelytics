from models import SessionLocal, UserModel, UserRole


def create_initial_users():
    session = SessionLocal()
    try:
        user_count = session.query(UserModel).count()
        if user_count > 0:
            return

        admin_user = UserModel(
            nombre="Acadelytics",
            apellido="Admin",
            correo="admin@acadelytics.com",
            rol=UserRole.Admin,
            role_changes_remaining=3,
        )
        admin_user.set_password("admin1234")

        alumno_user = UserModel(
            nombre="Alumno",
            apellido="Ejemplo",
            correo="alumno@acadelytics.com",
            rol=UserRole.Alumno,
            role_changes_remaining=3,
        )
        alumno_user.set_password("alumno1234")

        profesor_user = UserModel(
            nombre="Profesor",
            apellido="Ejemplo",
            correo="profesor@acadelytics.com",
            rol=UserRole.Profesor,
            role_changes_remaining=3,
        )
        profesor_user.set_password("profesor1234")

        session.add_all([admin_user, alumno_user, profesor_user])
        session.commit()

        print("=> Usuarios iniciales creados exitosamente")
    except Exception as error:
        session.rollback()
        print(f"Error al crear usuarios iniciales: {error}")
    finally:
        session.close()
