from flask import Flask
from flask_cors import CORS
from config.configEnv import HOST, PORT
from config.configDb import connect_db
from config.initial_setup import create_initial_users
from models import init_db
from routes import register_routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4173", "http://127.0.0.1:4173"], "supports_credentials": True}})
register_routes(app)

connect_db()
init_db()
create_initial_users()

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Backend activo'}


def main():
    connect_db()
    init_db()
    create_initial_users()
    app.run(host=HOST or '0.0.0.0', port=int(PORT or 5000), debug=False)


if __name__ == '__main__':
    main()
