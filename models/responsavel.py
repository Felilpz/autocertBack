from db.connection import db


class Responsavel(db.Model):
    __tablename__ = 'responsaveis'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)

    # Definindo o relacionamento com Loja via a tabela intermediária LojaResponsavel
    lojas = db.relationship(
        'Loja', secondary='loja_responsavel', back_populates='responsaveis')
