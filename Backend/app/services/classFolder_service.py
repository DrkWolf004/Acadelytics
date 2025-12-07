from app.models.classFolder_model import ClassFolder
from app.models.classroom_model import Classroom
from app import db
from sqlalchemy import or_
from typing import Tuple, Optional, List, Dict, Any

def get_classfolder_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        cf_id = query.get('id')
        classroom_id = query.get('classroom_id')

        filters = []
        if cf_id:
            try:
                filters.append(ClassFolder.id == int(cf_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if classroom_id:
            try:
                filters.append(ClassFolder.classroom_id == int(classroom_id))
            except Exception:
                return None, "classroom_id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar al menos id o classroom_id"

        cf_obj = ClassFolder.query.filter(or_(*filters)).first()
        if not cf_obj:
            return None, "ClassFolder no encontrado"

        data = {
            'id': cf_obj.id,
            'classroom_id': cf_obj.classroom_id,
            'created_at': cf_obj.created_at,
            'updated_at': cf_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error obtener el classFolder:", error)
        return None, "Error interno del servidor"


def get_classfolders_service() -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        cf_list = ClassFolder.query.all()
        if not cf_list:
            return [], None

        data_list = []
        for cf in cf_list:
            data_list.append({
                'id': cf.id,
                'classroom_id': cf.classroom_id,
                'created_at': cf.created_at,
                'updated_at': cf.updated_at
            })
        return data_list, None
    except Exception as error:
        print("Error al obtener los classFolders:", error)
        return None, "Error interno del servidor"


def create_classfolder_service(body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        classroom_id = body.get('classroom_id')
        if classroom_id is None or classroom_id == '':
            return None, "classroom_id es requerido"
        try:
            cid = int(classroom_id)
            if cid <= 0:
                raise ValueError()
        except Exception:
            return None, "classroom_id debe ser un entero positivo"

        classroom_obj = Classroom.query.get(cid)
        if not classroom_obj:
            return None, "Classroom asociado no encontrado"

        cf_obj = ClassFolder(classroom_id=cid)
        db.session.add(cf_obj)
        db.session.commit()

        data = {
            'id': cf_obj.id,
            'classroom_id': cf_obj.classroom_id,
            'created_at': cf_obj.created_at,
            'updated_at': cf_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al crear classFolder:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def update_classfolder_service(query: Dict[str, Any], body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        cf_id = query.get('id')
        filters = []
        if cf_id:
            try:
                filters.append(ClassFolder.id == int(cf_id))
            except Exception:
                return None, "id debe ser un entero válido"
        else:
            classroom_q = query.get('classroom_id')
            if classroom_q:
                try:
                    filters.append(ClassFolder.classroom_id == int(classroom_q))
                except Exception:
                    return None, "classroom_id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar id o classroom_id para identificar el classFolder"

        cf_obj = ClassFolder.query.filter(or_(*filters)).first()
        if not cf_obj:
            return None, "ClassFolder no encontrado"

        
        if 'classroom_id' in body and body.get('classroom_id') is not None:
            try:
                new_cid = int(body.get('classroom_id'))
                if new_cid <= 0:
                    raise ValueError()
            except Exception:
                return None, "classroom_id debe ser un entero positivo"
            classroom_obj = Classroom.query.get(new_cid)
            if not classroom_obj:
                return None, "Classroom asociado no encontrado"
            cf_obj.classroom_id = new_cid

        db.session.commit()

        data = {
            'id': cf_obj.id,
            'classroom_id': cf_obj.classroom_id,
            'created_at': cf_obj.created_at,
            'updated_at': cf_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al modificar un classFolder:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def delete_classfolder_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        cf_id = query.get('id')
        classroom_q = query.get('classroom_id')

        filters = []
        if cf_id:
            try:
                filters.append(ClassFolder.id == int(cf_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if classroom_q:
            try:
                filters.append(ClassFolder.classroom_id == int(classroom_q))
            except Exception:
                return None, "classroom_id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar al menos id o classroom_id"

        cf_obj = ClassFolder.query.filter(or_(*filters)).first()
        if not cf_obj:
            return None, "ClassFolder no encontrado"

        db.session.delete(cf_obj)
        db.session.flush()  

        classroom_obj = Classroom.query.get(cf_obj.classroom_id)
        if classroom_obj:
            remaining = ClassFolder.query.filter_by(classroom_id=classroom_obj.id).count()
            if remaining == 0:
                db.session.delete(classroom_obj)
            else:
                pass

        db.session.commit()

        data = {
            'id': cf_obj.id,
            'classroom_id': cf_obj.classroom_id,
            'created_at': cf_obj.created_at,
            'updated_at': cf_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al eliminar un classFolder:", error)
        db.session.rollback()
        return None, "Error interno del servidor"
