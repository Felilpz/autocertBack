from flask import Blueprint, jsonify, request
from models.loja import Loja
from models.responsavel import Responsavel
from models.loja_responsavel import LojaResponsavel
from db.connection import db

loja_routes = Blueprint('loja_routes', __name__)


@loja_routes.route('/lojas', methods=['GET'])
def get_lojas():
    lojas = Loja.query.all()
    return jsonify([{
        'id': loja.id,
        'cnpj': loja.cnpj,
        'razaosocial': loja.razaosocial,
        'bandeira': loja.bandeira,
        'validade_certificado': loja.validade_certificado
    } for loja in lojas])


@loja_routes.route('/lojas', methods=['POST'])
def create_loja():
    data = request.get_json()

    if not data or 'cnpj' not in data or 'razaosocial' not in data:
        return jsonify({'message': 'CNPJ e Razao Social são obrigatórios'}), 400

    cnpj = data['cnpj']
    razaosocial = data['razaosocial']
    bandeira = data.get('bandeira')
    validade_certificado = data.get('validade_certificado')

    loja = Loja(cnpj=cnpj, razaosocial=razaosocial, bandeira=bandeira,
                validade_certificado=validade_certificado)

    try:
        db.session.add(loja)
        db.session.commit()
        return jsonify({'message': 'loja adicionada com sucesso', 'id': loja.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao adicionar loja', 'error': str(e)}), 500


@loja_routes.route('/responsaveis', methods=['GET'])
def get_responsaveis():
    responsaveis = Responsavel.query.all()
    return jsonify([{
        'id': responsavel.id,
        'nome': responsavel.nome,
        'telefone': responsavel.telefone,
        'email': responsavel.email
    } for responsavel in responsaveis])


@loja_routes.route('/associar_responsavel', methods=['POST'])
def associar_responsavel():
    loja_id = request.json.get('loja_id')
    responsavel_id = request.json.get('responsavel_id')

    loja = Loja.query.get(loja_id)
    responsavel = Responsavel.query.get(responsavel_id)

    if loja and responsavel:
        loja_responsavel = LojaResponsavel(
            loja_id=loja.id, responsavel_id=responsavel.id)
        db.session.add(loja_responsavel)
        db.session.commit()
        return jsonify({'message': 'responsavel associado à loja com sucesso!'}), 201

    return jsonify({'message': 'loja ou responsavel não encontrados!'}), 404
