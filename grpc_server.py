from concurrent import futures
import grpc
import redis

import transfer_pb2_grpc
import transfer_pb2


class TransferServer(transfer_pb2_grpc.TransferServicer):

    def __init__(self, comm_host="localhost", comm_port=8888, redis_host='localhost', redis_port=6379):
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def transfer(self, request, context):
        response = transfer_pb2.Response()
        try:
            self.r.rpush(str(request.party_number), request.value)
        except Exception as e:
            print(e)
        finally:
            response.value = 200
            return response


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transfer_pb2_grpc.add_TransferServicer_to_server(TransferServer(), server)
    server.add_insecure_port("[::]:8888")
    server.start()
    server.wait_for_termination()