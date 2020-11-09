from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from model import db
from util import config


app = Flask(__name__, static_folder='/app/ui', static_url_path='/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
db.init_app(app)
CORS(app)


"""
Import module API routes
"""
from rpgmanager import api

"""
Offer React pages
"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@app.errorhandler(404)
def index(path):
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()