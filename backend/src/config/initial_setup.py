import os

from sqlalchemy import text

from models import SessionLocal, UserModel, UserRole
from models.professor_validation_model import ProfessorValidationRequestModel


def create_uploads_folder():
    """Ensure uploads folder exists."""
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"=> Carpeta de uploads disponible en: {uploads_dir}")


def ensure_file_uploaded_by_column_exists():
    """Add the uploaded_by_id column to existing files tables when needed."""
    session = SessionLocal()
    try:
        session.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS uploaded_by_id INTEGER"))
        session.commit()
        print("=> Columna uploaded_by_id verificada en la tabla files")
    except Exception as error:
        session.rollback()
        print(f"Error al verificar la columna uploaded_by_id: {error}")
    finally:
        session.close()


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
