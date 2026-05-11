# Acadelytics

Acadelytics es una plataforma educativa que emplea Machine Learning para ofrecer aprendizaje adaptativo mediante ejercicios personalizados. El sistema transforma la planificación docente en datos en tiempo real para optimizar el seguimiento académico y corregir brechas de conocimiento antes de las evaluaciones.

## Lenguajes utilizados
- Python
- JavaScript
- TypeScript
- SQL

## Arquitectura
- Base de datos: PostgreSQL
- Backend: Flask
- Frontend: React

## Inicio rápido
```bash
git clone https://github.com/DrkWolf004/Acadelytics.git
cd Acadelytics
docker compose up
```

## Estructura del proyecto
```
Acadelytics/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── app.py
│       ├── config/
│       │   ├── configDb.py
│       │   ├── configEnv.py
│       │   ├── initial_setup.py
│       │   └── .env.example
│       ├── controllers/
│       ├── handlers/
│       ├── middlewares/
│       ├── models/
│       ├── routes/
│       ├── services/
│       └── validations/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── public/
│   └── src/
│       ├── main.ts
│       ├── counter.ts
│       ├── style.css
│       └── assets/
├── docker-compose.yml
└── README.md
```