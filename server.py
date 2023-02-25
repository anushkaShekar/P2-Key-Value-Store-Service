import grpc
from concurrent import futures
import numstore_pb2_grpc
import numstore_pb2

values = {}
total = 0
factorial = 1
i = 1

class NumStore(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, request, context):
        if request.key not in values:
            values[request.key] = request.value
            global total
            total = total + request.value
        elif request.value != values[request.key]:
            total = total - values[request.key]
            total = total + request.value
            values[request.key] = request.value
        return numstore_pb2.SetNumResp(total=total)

    def Fact(self, request, context):
        if request.key in values:
            global i
            while i <= values[request.key]:
                global factorial
                factorial = factorial * i
                i = i + 1
        else:
            print("Key can not be found")
        return numstore_pb2.FactResp(value=factorial)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])

numstore_pb2_grpc.add_NumStoreServicer_to_server(NumStore(), server)

server.add_insecure_port('localhost:5440')
server.start()
server.wait_for_termination()

