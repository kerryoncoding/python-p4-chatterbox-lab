from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
     
    if request.method == 'GET':
        message_sort = Message.query.order_by('created_at').all()
        message_serialized = [message.to_dict() for message in message_sort]

        response = make_response(
            message_serialized,
            200
        )
        return response
    elif request.method == 'POST':
        request_json = request.get_json()
        new_message = Message(
            body = request_json['body'],
            username = request_json['username']
        )
        db.session.add(new_message)
        db.session.commit()

        response_dict = new_message.to_dict()
        response = make_response(
            response_dict,
            201
        )
        return response

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message_update = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        request_json=request.get_json()
        for key in request_json:
            setattr(message_update, key, request_json[key])
        db.session.add(message_update)
        db.session.commit()

        response = make_response(
            message_update.to_dict(),
            200
        )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message_update)
        db.session.commit()
        
        response = make_response('', 204)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug = True)
