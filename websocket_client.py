import time
import redis
import socketio


class WebSocketClient:

    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:8888')

    def send(self, value, party_number):
        data = {"party_number": party_number, "value": value}
        self.sio.emit("transfer", data)

    def disconnect(self):
        self.sio.disconnect()


client = WebSocketClient()
start_time = time.time()
number_of_requests = 2000
for i in range(0, number_of_requests):
    client.send(i, 0)
    time.sleep(0.001)
end_time = time.time()
print("elapsed time for " + str(number_of_requests) + " requests is " + str(end_time - start_time) + " secs")
client.disconnect()
