from app import db
from sqlalchemy.sql import func
from app.models.user_model import user

class Classroom(db.Model):
    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    member = db.relationship('user', backref=db.backref('classrooms', lazy=True))

    classfolders = db.relationship(
        'ClassFolder',
        backref=db.backref('classroom', lazy=True),
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )