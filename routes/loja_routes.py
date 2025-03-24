from flask import Blueprint, jsonify, request
from models.loja import Loja
from models.responsavel import Responsavel
from models.loja_responsavel import LojaResponsavel
from db.connection import db
import uuid

loja_routes = Blueprint('loja_routes', __name__)

# pegar dados
@loja_routes.route('/lojas', methods=['GET'])
def get_lojas():
    lojas = Loja.query.all()
    return jsonify([{
        'id': str(loja.id),  # Convert UUID to string for JSON
        'cnpj': loja.cnpj,
        'razaosocial': loja.razaosocial,
        'bandeira': loja.bandeira,
        'validade_certificado': loja.validade_certificado,
        'telefone': loja.telefone,
        'email': loja.email,
        'responsavel': loja.responsavel
    } for loja in lojas])

# enviar dados
@loja_routes.route('/lojas', methods=['POST'])
def create_loja():
    data = request.get_json()
    print(data)

    if not data or 'cnpj' not in data or 'razaoSocial' not in data or 'telefone' not in data or 'email' not in data:
        return jsonify({'message': 'CNPJ, Razao Social, Telefone e Email são obrigatórios'}), 400

    cnpj = data['cnpj']
    razaosocial = data['razaoSocial']
    bandeira = data.get('bandeira')
    validade_certificado = None
    telefone = data['telefone']
    email = data['email']
    responsavel = data.get('responsavel')
    

    loja = Loja(cnpj=cnpj, razaosocial=razaosocial, bandeira=bandeira,
                validade_certificado=validade_certificado, telefone=telefone, email=email, responsavel=responsavel)
    try:
        db.session.add(loja)
        db.session.commit()
        return jsonify({'message': 'loja adicionada com sucesso', 'id': str(loja.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao adicionar loja', 'error': str(e)}), 500