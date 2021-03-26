from flask import Flask, request, jsonify
import redis


app = Flask(__name__)


@app.route('/transfer',methods=["POST"])
def transfer_data():
    party_number = request.json["party_number"]
    value = request.json["value"]
    try:
        r.rpush(str(party_number), value)
    except Exception as e:
        print(e)
    return jsonify({"response": "200"})


if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    app.run(debug=False, host='0.0.0.0', port=8888)
