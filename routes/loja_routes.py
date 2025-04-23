from flask import Blueprint, jsonify, request
from models.loja import Loja
from db.connection import db
import uuid
from datetime import datetime

loja_routes = Blueprint('loja_routes', __name__)

# carregar lojas


@loja_routes.route('/lojas', methods=['GET'])
@loja_routes.route('/lojas', methods=['GET'])
def get_lojas():
    # Ordena as lojas pela data de validade do certificado (crescente)
    lojas = Loja.query.filter_by(ativo=True).order_by(
        Loja.validade_certificado).all()
    return jsonify([{
        'id': str(loja.id),
        'cnpj': loja.cnpj,
        'razaosocial': loja.razaosocial,
        'bandeira': loja.bandeira,
        'validade_certificado': loja.validade_certificado,
        'telefone': loja.telefone,
        'email': loja.email,
        'responsavel': loja.responsavel
    } for loja in lojas])


# Buscar loja por CNPJ (pra inativar dps)
@loja_routes.route('/lojas/cnpj/<string:cnpj>', methods=['GET'])
def get_loja_by_cnpj(cnpj):
    loja = Loja.query.filter_by(cnpj=cnpj).first()
    if loja:
        return jsonify({
            'id': str(loja.id),
            'cnpj': loja.cnpj,
            'razaosocial': loja.razaosocial,
            'bandeira': loja.bandeira,
            'validade_certificado': loja.validade_certificado,
            'telefone': loja.telefone,
            'email': loja.email,
            'responsavel': loja.responsavel,
            'ativo': loja.ativo
        }), 200
    else:
        return jsonify({'message': 'Loja não encontrada'}), 404

# enviar dados


@loja_routes.route('/lojas', methods=['POST'])
def create_loja():
    data = request.get_json()
    print(data)

    if not data or 'cnpj' not in data or 'razaoSocial' not in data or 'telefone' not in data or 'email' not in data or 'validade_certificado' not in data:
        return jsonify({'message': 'Todos os são obrigatórios'}), 400

    cnpj = data['cnpj']
    razaosocial = data['razaoSocial']
    bandeira = data.get('bandeira')
    validade_certificado = datetime.strptime(
        data.get('validade_certificado'), '%d-%m-%Y')
    telefone = data['telefone']
    email = data['email']
    responsavel = data.get('responsavel')

    print(validade_certificado)

    loja = Loja(cnpj=cnpj, razaosocial=razaosocial, bandeira=bandeira,
                validade_certificado=validade_certificado, telefone=telefone, email=email, responsavel=responsavel)
    cnpjExistente = Loja.query.filter_by(cnpj=cnpj).first()
    if cnpjExistente:
        return jsonify({
            'message': 'CNPJ Já Cadastrado',
            'status': 'Loja Ativa' if cnpjExistente.ativo else 'Loja Inativa',
            'cnpj': cnpjExistente.cnpj
        }), 409
    
    try:
        db.session.add(loja)
        db.session.commit()
        return jsonify({'message': 'loja adicionada com sucesso', 'id': str(loja.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao adicionar loja', 'error': str(e)}), 500


# desativar loja
@loja_routes.route('/lojas/desativar', methods=['PUT'])
def desativar_loja():
    data = request.get_json()

    if not data or 'cnpj' not in data:
        return jsonify({'message': 'CNPJ é obrigatório'}), 400

    loja = Loja.query.filter_by(cnpj=data['cnpj']).first()

    if not loja:
        return jsonify({'message': 'Loja não encontrada'}), 404

    loja.ativo = False
    try:
        db.session.commit()
        return jsonify({'message': 'Loja desativada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao desativar loja', 'error': str(e)}), 500

# Atualizar loja por CNPJ


@loja_routes.route('/lojas/<string:cnpj>', methods=['PUT'])
def update_loja(cnpj):
    data = request.get_json()

    loja = Loja.query.filter_by(cnpj=cnpj).first()
    if not loja:
        return jsonify({'message': 'Loja não encontrada'}), 404

    if 'razaosocial' in data:
        loja.razaosocial = data['razaosocial']
    if 'bandeira' in data:
        loja.bandeira = data['bandeira']
    if 'validade_certificado' in data:
        try:
            loja.validade_certificado = datetime.strptime(
                data['validade_certificado'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
    if 'telefone' in data:
        loja.telefone = data['telefone']
    if 'email' in data:
        loja.email = data['email']
    if 'responsavel' in data:
        loja.responsavel = data['responsavel']
        novo_cnpj = cnpj

    if 'cnpj' in data and data['cnpj'] != cnpj:
        novo_cnpj = data['cnpj']
        print(f"Tentando alterar CNPJ de {cnpj} para {novo_cnpj}")

        loja_existente = Loja.query.filter_by(cnpj=novo_cnpj).first()
        if loja_existente:
            print(f"Já existe uma loja com CNPJ {novo_cnpj}")
            return jsonify({'message': 'Já existe uma loja com este CNPJ'}), 409

        print(f"Atualizando CNPJ para {novo_cnpj}")
        loja.cnpj = novo_cnpj
        print(loja.validade_certificado)

    try:
        db.session.commit()
        return jsonify({
            'message': 'Loja atualizada com sucesso',
            'id': str(loja.id),
            'cnpj': loja.cnpj,
            'validade_certificado': loja.validade_certificado.strftime('%Y-%m-%d')
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar loja', 'error': str(e)}), 500
