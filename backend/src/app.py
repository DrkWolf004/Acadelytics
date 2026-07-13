from flask import Flask
from flask_cors import CORS
from config.configEnv import HOST, PORT, CORS_ORIGINS
from config.configDb import connect_db
from config.initial_setup import create_initial_users, create_uploads_folder, ensure_file_uploaded_by_column_exists, ensure_homework_responses_columns_exist
from services.professor_validation_service import ensure_prof_validation_dir_exists
from models import init_db
from routes import register_routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS, "supports_credentials": True}})
register_routes(app)

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Backend activo'}

@app.before_request
def initialize_db():
    if not hasattr(app, '_db_initialized'):
        try:
            create_uploads_folder()
            ensure_prof_validation_dir_exists()
            connect_db()
            init_db()
            ensure_file_uploaded_by_column_exists()
            ensure_homework_responses_columns_exist()
            create_initial_users()
            app._db_initialized = True
        except Exception as e:
            print(f"Error inicializando BD: {e}")
            return {'status': 'error', 'message': 'Error de base de datos'}, 503

def main():
    try:
        create_uploads_folder()
        ensure_prof_validation_dir_exists()
        connect_db()
        init_db()
        ensure_file_uploaded_by_column_exists()
        ensure_homework_responses_columns_exist()
        create_initial_users()
    except Exception as e:
        print(f"Advertencia inicial: {e}")

    app.run(host=HOST or '0.0.0.0', port=int(PORT or 5000), debug=False)


if __name__ == '__main__':
    main()
