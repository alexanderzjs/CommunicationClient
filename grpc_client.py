import time
import grpc
import redis

import transfer_pb2_grpc
import transfer_pb2


class GrpcClient:

    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        channel = grpc.insecure_channel("localhost:8888")
        self.stub = transfer_pb2_grpc.TransferStub(channel)

    def send(self, value, party_number):
        data = transfer_pb2.Request(party_number=party_number, value=value)
        response = self.stub.transfer(data)
        if response.value != 200:
            raise Exception("server has some exceptions")

    def disconnect(self):
        pass


client = GrpcClient()
start_time = time.time()
number_of_requests = 2000
for i in range(0, number_of_requests):
    client.send(i, 0)
end_time = time.time()
print("elapsed time for " + str(number_of_requests) + " requests is " + str(end_time - start_time) + " secs")
client.disconnect()