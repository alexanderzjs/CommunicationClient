import time
import requests
import redis


class RestClient:

    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def send(self, value, party_number):
        data = {"party_number": party_number, "value": value}
        response = requests.post("http://localhost:8888/transfer", json=data)
        if response.ok is False:
            raise Exception("cannot send to server")


client = RestClient()
start_time = time.time()
number_of_requests = 2000
for i in range(0, number_of_requests):
    client.send(i, 0)
end_time = time.time()
print("elapsed time for " + str(number_of_requests) + " requests is " + str(end_time - start_time) + " secs")
