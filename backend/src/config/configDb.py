from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .configEnv import DATABASE, DB_USERNAME, DB_HOST, PASSWORD

DATABASE_URL = f"postgresql://{DB_USERNAME}:{PASSWORD}@{DB_HOST}:5432/{DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def connect_db():
    try:
        engine.connect()
        print("=> Conexión exitosa a la base de datos!")
    except Exception as error:
        print(f"Error al conectar con la base de datos: {error}")
        exit(1)