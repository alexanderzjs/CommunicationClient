import redis
from flask import Flask
from flask_socketio import send, SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('transfer')
def transfer(json, methods=['GET', 'POST']):
    party_number = json["party_number"]
    value = json["value"]
    try:
        r.rpush(str(party_number), value)
    except Exception as e:
        print(e)
    return 200


if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    socketio.run(host="0.0.0.0", port=8888, debug=True, app=app)
