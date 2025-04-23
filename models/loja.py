from db.connection import db
import uuid

class Loja(db.Model):
    __tablename__ = 'lojas'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    razaosocial = db.Column(db.String(255), nullable=False)
    bandeira = db.Column(db.String(100))
    validade_certificado = db.Column(db.Date)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
