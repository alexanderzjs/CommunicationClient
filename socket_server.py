import socket
import redis
import json


def start_service(host, port, redis):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        while True:
            size = 0
            DATA_SIZE = 55
            accumulated_data = ''
            while size < DATA_SIZE:
                data = bytes.decode(conn.recv(55), encoding='utf-8')
                if len(data) == 0:
                    break
                accumulated_data += data
                size += len(data)
            if size < DATA_SIZE:
                break
            json_obj = json.loads(accumulated_data)
            party_number = json_obj["party_number"]
            value = json_obj["value"]
            try:
                redis.rpush(str(int(party_number, 16)), int(value, 16))
            except Exception as e:
                print(e)

if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    start_service("0.0.0.0", 8888, r)
