from datetime import datetime
from app import db

class Fio(db.Model):
    __tablename__ = 'fios'
    id = db.Column(db.String, primary_key=True)
    marca = db.Column(db.String, nullable=True)
    cor = db.Column(db.String, nullable=True)
    espessura = db.Column(db.String, nullable=True)
    gramas = db.Column(db.Integer, default=0)
    foto = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ideia(db.Model):
    __tablename__ = 'ideias'
    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=True)
    cor_requerida = db.Column(db.String, nullable=True)
    espessura_requerida = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    progresso = db.Column(db.Integer, default=0)
    notas = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)