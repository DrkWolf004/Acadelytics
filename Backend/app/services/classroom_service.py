from app.models.classroom_model import Classroom
from app.models.classFolder_model import ClassFolder
from app.models.user_model import user
from app import db
from sqlalchemy import or_
from typing import Tuple, Optional, List, Dict, Any
from datetime import datetime

def get_classroom_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        classroom_id = query.get('id')
        nombre = query.get('nombre')
        member_id = query.get('member_id')

        filters = []
        if classroom_id:
            try:
                filters.append(Classroom.id == int(classroom_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if nombre:
            filters.append(Classroom.nombre == nombre)
        if member_id:
            try:
                filters.append(Classroom.member_id == int(member_id))
            except Exception:
                return None, "member_id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar al menos id, nombre o member_id"

        classroom_obj = Classroom.query.filter(or_(*filters)).first()

        if not classroom_obj:
            return None, "Classroom no encontrado"

        data = {
            'id': classroom_obj.id,
            'nombre': classroom_obj.nombre,
            'member_id': classroom_obj.member_id,
            'created_at': classroom_obj.created_at,
            'updated_at': classroom_obj.updated_at
        }

        return data, None
    except Exception as error:
        print("Error obtener el classroom:", error)
        return None, "Error interno del servidor"


def get_classrooms_service() -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        classrooms_list = Classroom.query.all()
        if not classrooms_list:
            return [], None

        data_list = []
        for cls in classrooms_list:
            data_list.append({
                'id': cls.id,
                'nombre': cls.nombre,
                'member_id': cls.member_id,
                'created_at': cls.created_at,
                'updated_at': cls.updated_at
            })

        return data_list, None
    except Exception as error:
        print("Error al obtener los classrooms:", error)
        return None, "Error interno del servidor"


def create_classroom_service(body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        nombre = body.get('nombre')
        member_id = body.get('member_id')

        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            return None, "nombre es requerido"
        if member_id is None or member_id == '':
            return None, "member_id es requerido"
        try:
            mid = int(member_id)
            if mid <= 0:
                raise ValueError()
        except Exception:
            return None, "member_id debe ser un entero positivo"

        member_obj = user.query.get(mid)
        if not member_obj:
            return None, "Miembro (user) no encontrado"

        classroom_obj = Classroom(nombre=nombre.strip(), member_id=mid)
        db.session.add(classroom_obj)
        db.session.flush()

        # Crear y vincular ClassFolder para este classroom
        cf_obj = ClassFolder(classroom_id=classroom_obj.id)
        db.session.add(cf_obj)
        db.session.commit()

        data = {
            'id': classroom_obj.id,
            'nombre': classroom_obj.nombre,
            'member_id': classroom_obj.member_id,
            'classfolder_id': cf_obj.id,
            'created_at': classroom_obj.created_at,
            'updated_at': classroom_obj.updated_at
        }

        return data, None
    except Exception as error:
        print("Error al crear classroom:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def update_classroom_service(query: Dict[str, Any], body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        classroom_id = query.get('id')
        nombre_q = query.get('nombre')

        filters = []
        if classroom_id:
            try:
                filters.append(Classroom.id == int(classroom_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if nombre_q:
            filters.append(Classroom.nombre == nombre_q)

        if not filters:
            return None, "Debe proporcionar al menos id o nombre para identificar el classroom"

        classroom_obj = Classroom.query.filter(or_(*filters)).first()
        if not classroom_obj:
            return None, "Classroom no encontrado"

        
        if 'member_id' in body and body.get('member_id') is not None:
            try:
                mid = int(body.get('member_id'))
                if mid <= 0:
                    raise ValueError()
            except Exception:
                return None, "member_id debe ser un entero positivo"
            member_obj = user.query.get(mid)
            if not member_obj:
                return None, "Miembro (user) no encontrado"
            classroom_obj.member_id = mid

        if 'nombre' in body and body.get('nombre') is not None:
            nombre_body = body.get('nombre')
            if isinstance(nombre_body, str) and nombre_body.strip() != '':
                classroom_obj.nombre = nombre_body.strip()

        db.session.commit()

        data = {
            'id': classroom_obj.id,
            'nombre': classroom_obj.nombre,
            'member_id': classroom_obj.member_id,
            'created_at': classroom_obj.created_at,
            'updated_at': classroom_obj.updated_at
        }

        return data, None
    except Exception as error:
        print("Error al modificar un classroom:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def delete_classroom_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        classroom_id = query.get('id')
        nombre = query.get('nombre')

        filters = []
        if classroom_id:
            try:
                filters.append(Classroom.id == int(classroom_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if nombre:
            filters.append(Classroom.nombre == nombre)

        if not filters:
            return None, "Debe proporcionar al menos id o nombre"

        classroom_obj = Classroom.query.filter(or_(*filters)).first()
        if not classroom_obj:
            return None, "Classroom no encontrado"

        db.session.delete(classroom_obj)
        db.session.commit()

        data = {
            'id': classroom_obj.id,
            'nombre': classroom_obj.nombre,
            'member_id': classroom_obj.member_id,
            'created_at': classroom_obj.created_at,
            'updated_at': classroom_obj.updated_at
        }

        return data, None
    except Exception as error:
        print("Error al eliminar un classroom:", error)
        db.session.rollback()
        return None, "Error interno del servidor"