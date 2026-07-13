

Acadelytics es una plataforma educativa que emplea Machine Learning para ofrecer aprendizaje adaptativo mediante ejercicios personalizados. El sistema transforma la planificación docente en datos en tiempo real para optimizar el seguimiento académico y corregir brechas de conocimiento antes de las evaluaciones.


- Python
- JavaScript
- TypeScript
- SQL


- Base de datos: PostgreSQL
- Backend: Flask
- Frontend: TypeScript + Vite


```bash
git clone https://github.com/DrkWolf004/Acadelytics.git
cd Acadelytics
docker compose up
```

La aplicación estará disponible en http://localhost:4173


- Base de datos: 5432 (interno)
- Backend: 5000
- Frontend: 4173



| Correo | Contraseña | Rol |
|--------|-----------|-----|
| admin@acadelytics.com | admin1234 | Admin |
| profesor@acadelytics.com | profesor1234 | Profesor |
| alumno@acadelytics.com | alumno1234 | Alumno |


```
Acadelytics/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── wait-for-db.sh
│   ├── uploads/
│   │   └── {class_folder_id}/
│   │       └── {uuid_filename}
│   └── src/
│       ├── app.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── configDb.py
│       │   ├── configEnv.py
│       │   └── initial_setup.py
│       ├── controllers/
│       │   ├── __init__.py
│       │   ├── class_folder_controller.py
│       │   ├── classroom_controller.py
│       │   ├── classroom_invitation_controller.py
│       │   ├── file_controller.py
│       │   ├── homework_controller.py
│       │   ├── professor_validation_controller.py
│       │   └── user_controller.py
│       ├── handlers/
│       │   └── response_handlers.py
│       ├── middlewares/
│       │   ├── __init__.py
│       │   ├── authentication.py
│       │   └── authorization.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── class_folder_model.py
│       │   ├── classroom_invitation_model.py
│       │   ├── classroom_model.py
│       │   ├── classroom_student_model.py
│       │   ├── file_model.py
│       │   ├── homework_model.py
│       │   ├── homework_response_model.py
│       │   ├── professor_validation_model.py
│       │   └── user_model.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── auth_routes.py
│       │   ├── class_folder_routes.py
│       │   ├── classroom_invitation_routes.py
│       │   ├── classroom_routes.py
│       │   ├── file_routes.py
│       │   ├── homework_routes.py
│       │   ├── professor_validation_routes.py
│       │   └── user_routes.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── auth_service.py
│       │   ├── class_folder_service.py
│       │   ├── classroom_invitation_service.py
│       │   ├── classroom_service.py
│       │   ├── file_service.py
│       │   ├── homework_service.py
│       │   ├── professor_validation_service.py
│       │   └── user_service.py
│       └── validations/
│           ├── __init__.py
│           ├── class_folder_validation.py
│           ├── classroom_invitation_validation.py
│           ├── classroom_validation.py
│           ├── file_validation.py
│           ├── homework_validation.py
│           └── user_validation.py
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── public/
│   └── src/
│       ├── app.ts
│       ├── fileUpload.ts
│       ├── hooks/
│       │   └── useLocalStorage.ts
│       ├── main.ts
│       ├── modal.ts
│       ├── style.css
│       ├── types.ts
│       ├── pages/
│       │   ├── admin.ts
│       │   ├── classrooms.ts
│       │   ├── dashboard.ts
│       │   ├── home.ts
│       │   ├── homework.ts
│       │   ├── login.ts
│       │   ├── professorValidation.ts
│       │   ├── profile.ts
│       │   └── register.ts
│       └── services/
│           ├── api.ts
│           ├── authService.ts
│           ├── classroomService.ts
│           ├── fileService.ts
│           ├── homeworkService.ts
│           ├── invitationService.ts
│           ├── professorValidationService.ts
│           └── userService.ts
```
