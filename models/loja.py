from db.connection import db


class Loja(db.Model):
    __tablename__ = 'lojas'

    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    razaosocial = db.Column(db.String(255), nullable=False)
    bandeira = db.Column(db.String(255), nullable=True)
    validade_certificado = db.Column(db.Date, nullable=True)

    # Definindo o relacionamento com Responsavel via a tabela intermediária LojaResponsavel
    responsaveis = db.relationship(
        'Responsavel', secondary='loja_responsavel', back_populates='lojas')
