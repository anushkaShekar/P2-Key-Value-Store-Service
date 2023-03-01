import grpc
import threading
from concurrent import futures
import numstore_pb2_grpc
import numstore_pb2

values = {}
total = 0
factorial = 1
i = 1
cache_size = 10
cache = {} # key is the value corresponding to the key request, value is the factorial of that value
lock = threading.Lock()

class NumStore(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, request, context):
        with lock:
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
            print("HELLO")
            val = values[request.key]
            print("HELLO")
            # Eviction policy: LRU
            if val in cache:
                hit = True
                fact = cache[val]
                cache.pop(val)
                cache[val] = fact
            else:
                hit = False
                global i
                while i <= val:
                    global factorial
                    factorial = factorial * i
                    i += 1
                cache[val] = factorial
                if len(cache) > cache_size:
                    cache.pop(0)
            return numstore_pb2.FactResp(value=cache[val], hit=hit)
        else:
            return numstore_pb2.FactResp(error="HELLO")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])
numstore_pb2_grpc.add_NumStoreServicer_to_server(NumStore(), server)

server.add_insecure_port('localhost:5440')
server.start()
server.wait_for_termination()

