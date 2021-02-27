from functools import wraps
from flask import jsonify, request
import jwt

def token_verify(function: callable) -> callable:
    ''' Checking the valid Token and refreshing it. If not valid, return
        Info and stopping client request
        :parram - http request.headers: (Username / Token)
        :return - Json with the corresponding information.
    '''

    @wraps(function)
    def decorated(*arg, **kwargs):
        raw_token = request.headers.get('Authorization')
        token = raw_token.split()[1]
        uid = request.headers.get('uid')

        # Caso sem token
        if not token:
            return jsonify({
                'error': 'Nao Autorizado'
            }), 401

        try:
            token_information = jwt.decode(token, key='1234', algorithms="HS256")
            token_uid = token_information['uid']

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

        if uid and token_uid and (int(token_uid) != int(uid)):
            return jsonify({
                'message': 'User not althorize',
                'status': False
            }), 403

        return function(token, *arg, **kwargs)

    return decorated
