from flask import Flask
from flask_cors import CORS
from .route import route_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(route_bp)
