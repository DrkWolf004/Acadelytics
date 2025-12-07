from app import db
from sqlalchemy.sql import func
from app.models.user_model import user

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(1024), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('user', backref=db.backref('files', lazy=True))

    classfolder_id = db.Column(db.Integer, db.ForeignKey('class_folders.id', ondelete='CASCADE'), nullable=False)
    classfolder = db.relationship('ClassFolder', backref=db.backref('files', lazy=True))

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )