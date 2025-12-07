from app.models.file_model import File
from app.models.classFolder_model import ClassFolder
from app.models.user_model import user
from app import db
from sqlalchemy import or_
from typing import Tuple, Optional, List, Dict, Any

def get_file_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        file_id = query.get('id')
        creator_id = query.get('creator_id')
        classfolder_id = query.get('classfolder_id')

        filters = []
        if file_id:
            try:
                filters.append(File.id == int(file_id))
            except Exception:
                return None, "id debe ser un entero válido"
        if creator_id:
            try:
                filters.append(File.creator_id == int(creator_id))
            except Exception:
                return None, "creator_id debe ser un entero válido"
        if classfolder_id:
            try:
                filters.append(File.classfolder_id == int(classfolder_id))
            except Exception:
                return None, "classfolder_id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar al menos id, creator_id o classfolder_id"

        file_obj = File.query.filter(or_(*filters)).first()
        if not file_obj:
            return None, "File no encontrado"

        data = {
            'id': file_obj.id,
            'file': file_obj.file,
            'creator_id': file_obj.creator_id,
            'classfolder_id': file_obj.classfolder_id,
            'created_at': file_obj.created_at,
            'updated_at': file_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error obtener el file:", error)
        return None, "Error interno del servidor"


def get_files_service() -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    try:
        files_list = File.query.all()
        if not files_list:
            return [], None

        data_list = []
        for f in files_list:
            data_list.append({
                'id': f.id,
                'file': f.file,
                'creator_id': f.creator_id,
                'classfolder_id': f.classfolder_id,
                'created_at': f.created_at,
                'updated_at': f.updated_at
            })
        return data_list, None
    except Exception as error:
        print("Error al obtener los files:", error)
        return None, "Error interno del servidor"


def create_file_service(body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        file_field = body.get('file')
        creator_id = body.get('creator_id')
        classfolder_id = body.get('classfolder_id')

        if not file_field or not isinstance(file_field, str) or not file_field.strip():
            return None, "file es requerido"
        if creator_id is None or creator_id == '':
            return None, "creator_id es requerido"
        if classfolder_id is None or classfolder_id == '':
            return None, "classfolder_id es requerido"

        try:
            cid = int(creator_id)
            if cid <= 0:
                raise ValueError()
        except Exception:
            return None, "creator_id debe ser un entero positivo"

        try:
            cfid = int(classfolder_id)
            if cfid <= 0:
                raise ValueError()
        except Exception:
            return None, "classfolder_id debe ser un entero positivo"

        creator_obj = user.query.get(cid)
        if not creator_obj:
            return None, "Usuario (creator) no encontrado"

        classfolder_obj = ClassFolder.query.get(cfid)
        if not classfolder_obj:
            return None, "ClassFolder asociado no encontrado"

        file_obj = File(file=file_field.strip(), creator_id=cid, classfolder_id=cfid)
        db.session.add(file_obj)
        db.session.commit()

        data = {
            'id': file_obj.id,
            'file': file_obj.file,
            'creator_id': file_obj.creator_id,
            'classfolder_id': file_obj.classfolder_id,
            'created_at': file_obj.created_at,
            'updated_at': file_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al crear file:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def update_file_service(query: Dict[str, Any], body: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        file_id = query.get('id')
        if not file_id:
            return None, "Debe proporcionar id para identificar el file"

        try:
            filters = [File.id == int(file_id)]
        except Exception:
            return None, "id debe ser un entero válido"

        file_obj = File.query.filter(or_(*filters)).first()
        if not file_obj:
            return None, "File no encontrado"

        if 'file' in body and body.get('file') is not None:
            fval = body.get('file')
            if isinstance(fval, str) and fval.strip() != '':
                file_obj.file = fval.strip()

        if 'creator_id' in body and body.get('creator_id') is not None:
            try:
                new_creator = int(body.get('creator_id'))
                if new_creator <= 0:
                    raise ValueError()
            except Exception:
                return None, "creator_id debe ser un entero positivo"
            creator_obj = user.query.get(new_creator)
            if not creator_obj:
                return None, "Usuario (creator) no encontrado"
            file_obj.creator_id = new_creator

        if 'classfolder_id' in body and body.get('classfolder_id') is not None:
            try:
                new_cfid = int(body.get('classfolder_id'))
                if new_cfid <= 0:
                    raise ValueError()
            except Exception:
                return None, "classfolder_id debe ser un entero positivo"
            classfolder_obj = ClassFolder.query.get(new_cfid)
            if not classfolder_obj:
                return None, "ClassFolder asociado no encontrado"
            file_obj.classfolder_id = new_cfid

        db.session.commit()

        data = {
            'id': file_obj.id,
            'file': file_obj.file,
            'creator_id': file_obj.creator_id,
            'classfolder_id': file_obj.classfolder_id,
            'created_at': file_obj.created_at,
            'updated_at': file_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al modificar un file:", error)
        db.session.rollback()
        return None, "Error interno del servidor"


def delete_file_service(query: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        file_id = query.get('id')

        filters = []
        if file_id:
            try:
                filters.append(File.id == int(file_id))
            except Exception:
                return None, "id debe ser un entero válido"

        if not filters:
            return None, "Debe proporcionar id"

        file_obj = File.query.filter(or_(*filters)).first()
        if not file_obj:
            return None, "File no encontrado"

        db.session.delete(file_obj)
        db.session.commit()

        data = {
            'id': file_obj.id,
            'file': file_obj.file,
            'creator_id': file_obj.creator_id,
            'classfolder_id': file_obj.classfolder_id,
            'created_at': file_obj.created_at,
            'updated_at': file_obj.updated_at
        }
        return data, None
    except Exception as error:
        print("Error al eliminar un file:", error)
        db.session.rollback()
        return None, "Error interno del servidor"