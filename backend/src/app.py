from flask import Flask
from config.configEnv import HOST, PORT
from config.configDb import connect_db

app = Flask(__name__)

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Backend activo'}


def main():
    connect_db()
    app.run(host=HOST or '0.0.0.0', port=int(PORT or 5000), debug=False)


if __name__ == '__main__':
    main()
