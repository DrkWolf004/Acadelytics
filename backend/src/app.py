from flask import Flask
from config.configEnv import HOST, PORT
from config.configDb import connect_db
from config.initial_setup import create_initial_users
from models import init_db
from routes import register_routes

app = Flask(__name__)
register_routes(app)

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
