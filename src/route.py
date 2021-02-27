from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
import time

route_bp = Blueprint('route', __name__)

@route_bp.route("/secret", methods=["GET"])
def secret_route():

    raw_token = request.headers.get('Authorization')
    token = raw_token.split()[1]
    print(token)
    
    # Caso sem token
    if not token:
        return jsonify({
            'error': 'Nao Autorizado'
        }), 401
    
    token_information = jwt.decode(token, key='1234', algorithms="HS256")
    print(token_information)


    # Devemos chegar aqui
    return jsonify({
        'data': 'Mensagem secreta'
    }), 200



@route_bp.route("/auth", methods=["POST"])
def authorization_route():

    token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }, key='1234', algorithm="HS256")

    return jsonify({
        'token': token
    }), 200