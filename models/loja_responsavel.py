from db.connection import db


class lojaResponsavel(db.Model):

    __tablename__ = 'loja_responsavel'

    id = db.Column(db.Integer, primary_key=True)
    loja_id = db.Column(db.Integer, db.ForeignKey(
        'lojas.id', ondelete='CASCADE'), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey(
        'responsaveis.id', ondelete='CASCADE'), nullable=False)
