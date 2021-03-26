import time
import redis
import socket
import json


class SocketClient:

    def __init__(self, comm_host='localhost', comm_port=8888, redis_host='localhost', redis_port=6379):
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((comm_host, comm_port))

    def send(self, value, party_number, l=64):
        value = value % (1 << l)
        data = json.dumps({"party_number": '0x{:02X}'.format(party_number), "value": '0x{:016X}'.format(value)})
        total_sent = 0
        while total_sent < len(data):
            sent = self.sock.send(bytes(data[total_sent:], encoding='utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent

    def disconnect(self):
        self.sock.close()


client = SocketClient()
start_time = time.time()
number_of_requests = 2000
for i in range(0, number_of_requests):
    client.send(i, 0)
    time.sleep(0.001)
end_time = time.time()
print("elapsed time for " + str(number_of_requests) + " requests is " + str(end_time - start_time) + " secs")
client.disconnect()
