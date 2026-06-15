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
- Frontend: TypeScript + Vite

## Inicio rápido
```bash
git clone https://github.com/DrkWolf004/Acadelytics.git
cd Acadelytics
docker compose up
```

La aplicación estará disponible en http://localhost:4173

## Puertos
- Base de datos: 5432 (interno)
- Backend: 5000
- Frontend: 4173

## Usuarios de Prueba (Creados Automáticamente)

| Correo | Contraseña | Rol |
|--------|-----------|-----|
| admin@acadelytics.com | admin1234 | Admin |
| profesor@acadelytics.com | profesor1234 | Profesor |
| alumno@acadelytics.com | alumno1234 | Alumno |

## Estructura del proyecto
```
Acadelytics/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── wait-for-db.sh
│   └── src/
│       ├── app.py
│       ├── config/
│       │   ├── configDb.py
│       │   ├── configEnv.py
│       │   ├── initial_setup.py
│       │   └── .env
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
│   └── src/
│       ├── app.ts
│       ├── pages/
│       │   ├── dashboard.ts
│       │   ├── profile.ts
│       │   ├── admin.ts
│       │   ├── login.ts
│       │   ├── register.ts
│       │   └── home.ts
│       ├── services/
│       │   ├── api.ts
│       │   ├── authService.ts
│       │   └── userService.ts
│       └── hooks/
│           └── useLocalStorage.ts
├── docker-compose.yml
├── .env
├── .env.example
└── README.md
├── docker-compose.yml
└── README.md
```
