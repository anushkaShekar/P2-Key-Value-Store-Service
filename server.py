import grpc
from concurrent import futures
import numstore_pb2_grpc
import numstore_pb2

values = {}
total = 0

class NumStore(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, request, context):
        if request.key not in values:
            values[request.key] = request.value
            total = total + request.value
        return numstore_pb2.SetNumResp(total=total)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])

numstore_pb2_grpc.add_NumStoreServicer_to_server(NumStore(), server)

server.add_insecure_port('localhost:5440')
server.start()
server.wait_for_termination()

