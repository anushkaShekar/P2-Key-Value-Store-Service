import grpc
from concurrent import futures
import numstore_pb2_grpc

class NumStore(numstore_pb2_grpc.NumStoreServicer):
    def Temp(self, request, context):

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])
# TODO: add servicer


server.add_insecure_port('localhost:5444')
server.start()
server.wait_for_termination()

