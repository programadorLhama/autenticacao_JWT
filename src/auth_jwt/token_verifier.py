from functools import wraps
from flask import jsonify, request
import jwt
from .token_handler import token_creator

def token_verify(function: callable) -> callable:
    ''' Checking the valid Token and refreshing it. If not valid, return
        Info and stopping client request
        :parram - http request.headers: (Username / Token)
        :return - Json with the corresponding information.
    '''

    @wraps(function)
    def decorated(*arg, **kwargs):
        raw_token = request.headers.get('Authorization')
        uid = request.headers.get('uid')

        # Caso sem token
        if not raw_token or not uid:
            return jsonify({
                'error': 'Bad Request'
            }), 400

        try:
            token = raw_token.split()[1]
            token_information = jwt.decode(token, key='1234', algorithms="HS256")
            token_uid = token_information['uid']

        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Token is Expired!',
            }), 401

        except jwt.InvalidSignatureError:
            return jsonify({
                'message': 'Token is invalid',
            }), 401

        except KeyError as e:
            return jsonify({
                'message': 'Token is invalid',
            }), 401

        if uid and token_uid and (int(token_uid) != int(uid)):
            return jsonify({
                'message': 'User Unauthorized',
            }), 401

        next_token = token_creator.refresh(token)

        return function(next_token, *arg, **kwargs)

    return decorated
