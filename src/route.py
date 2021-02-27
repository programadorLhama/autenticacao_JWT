from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
import time

route_bp = Blueprint('route', __name__)

@route_bp.route("/secret", methods=["GET"])
def secret_route():

    UID = request.headers.get('UID')
    raw_token = request.headers.get('Authorization')
    token = raw_token.split()[1]
    
    # Caso sem token
    if not token:
        return jsonify({
            'error': 'Nao Autorizado'
        }), 401
    
    try:
        token_information = jwt.decode(token, key='1234', algorithms="HS256")
        token_UID = token_information['UID']

    except jwt.ExpiredSignatureError:
        return jsonify({
            'message': 'Token is Expired!',
            'status': False
        }), 403
    except jwt.InvalidSignatureError:
        return jsonify({
            'message': 'Token is invalid',
            'status': False
        }), 403
    except KeyError as e:
        return jsonify({
            'message': 'Token is invalid',
            'status': False
        }), 403

    if UID and token_UID and (int(token_UID) != int(UID)):
        return jsonify({
            'message': 'User not althorize',
            'status': False
        }), 403

    # Devemos chegar aqui
    return jsonify({
        'data': 'Mensagem secreta'
    }), 200



@route_bp.route("/auth", methods=["POST"])
def authorization_route():

    token = jwt.encode({
        'UID': 12,
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }, key='1234', algorithm="HS256")

    return jsonify({
        'token': token
    }), 200