from db.connection import db


class LojaResponsavel(db.Model):
    __tablename__ = 'loja_responsavel'

    id = db.Column(db.Integer, primary_key=True)
    loja_id = db.Column(db.Integer, db.ForeignKey(
        'lojas.id', ondelete='CASCADE'), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey(
        'responsaveis.id', ondelete='CASCADE'), nullable=False)

    # Relacionamentos reversos
    loja = db.relationship('Loja', backref=db.backref(
        'loja_responsavel', lazy='dynamic'))
    responsavel = db.relationship(
        'Responsavel', backref=db.backref('loja_responsavel', lazy='dynamic'))
