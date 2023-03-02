import grpc
import threading
import math
from concurrent import futures
import numstore_pb2_grpc
import numstore_pb2

values = {}
total = 0
cache_size = 10
cache = {} # key is the value corresponding to the key request, value is the factorial of that value
lock = threading.Lock()

class NumStore(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, request, context):
        with lock:
            if request.key not in values:
                values[request.key] = request.value
                global total
                total += request.value
            elif request.value != values[request.key]:
                total -= values[request.key]
                total += request.value
                values[request.key] = request.value
        return numstore_pb2.SetNumResp(total=total)

    def Fact(self, request, context):
        if request.key in values:
            val = values[request.key]
            # Eviction policy: LRU
            if val in cache:
                hit = True
                fact = cache[val]
                cache.pop(val)
                cache[val] = fact
            else:
                hit = False
                cache[val] = math.factorial(val)
                if len(cache) > cache_size:
                    cache.pop(next(iter(cache)))
            return numstore_pb2.FactResp(value=cache[val], hit=hit)
        else:
            return numstore_pb2.FactResp(error="Key does not exist.")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[("grpc.so_reuseport", 0)])
numstore_pb2_grpc.add_NumStoreServicer_to_server(NumStore(), server)

server.add_insecure_port('localhost:5440')
server.start()
server.wait_for_termination()

