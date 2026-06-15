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

## Características Principales

### Perfil de Usuario
- Ver y editar información personal sin mostrar contraseña
- Cambiar contraseña (soporta símbolos especiales)
- Cambiar rol (limitado a 3 cambios)
- Contador de cambios restantes visible

### Panel de Administrador (Solo Admin)
- Listar todos los usuarios del sistema
- Buscar usuarios por correo o ID
- Crear nuevos usuarios (popup)
- Editar usuarios (popup + selector de roles)
- Eliminar usuarios (con confirmación)
- Roles disponibles: Admin, Profesor, Alumno

### Navbar Mejorado
- Opción "Perfil" para ver y editar perfil personal
- Opción "Usuarios" visible solo para administradores
- Selector de tema claro/oscuro
- Panel de notificaciones

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
```

## Configuración de Entorno

El archivo `.env` en la raíz contiene las variables de entorno por defecto:
```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=acadelytics
BACKEND_PORT=5000
FRONTEND_PORT=4173
ACCESS_TOKEN_SECRET=supersecret_jwt_key_development
COOKIE_KEY=supersecret_cookie_key_development
```

Para cambiar puertos o credenciales, edita este archivo antes de ejecutar `docker compose up`.

## Solución de Problemas

### Puerto ya en uso
Si los puertos 5000 o 4173 ya están en uso, modifica el archivo `.env`:
```env
BACKEND_PORT=5001
FRONTEND_PORT=4174
```

### Base de datos corrupta o errores de conexión
Para limpiar y reiniciar todo:
```bash
docker compose down -v
docker compose up
```

Esto eliminará todos los volúmenes y recreará la base de datos desde cero.

### Error 500 en login
Asegúrate de que PostgreSQL esté completamente iniciado (espera ~10 segundos después de `docker compose up`).

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