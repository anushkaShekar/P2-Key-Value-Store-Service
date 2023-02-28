import sys
import grpc
import threading
import random, string
import numstore_pb2_grpc
import numstore_pb2

port = "5440"
addr = f"127.0.0.1:{port}"
channel = grpc.insecure_channel(addr)
stub = numstore_pb2_grpc.NumStoreStub(channel)

def task():
    key_list = []
    for i in range(100):
        val = random.choice(string.ascii_uppercase)
        key_list.append(val)

    #for i in range(8):
        #create_thread()
        #for i in range(100):
            #t.start()
            #t.join()

    return key_list

def create_thread():
    t = threading.Thread(target=thread_function)

def thread_function():
    keys = task()
    randomKey = random.choice(keys)
    randomValue = random.randint(1, 15)
    function_list = [stub.SetNum(numstore_pb2.SetNumRequest()), stub.Fact(numstore_pb2.FactRequest())]
    randomFunction = random.choice(function_list)

    if randomFunction == stub.SetNum(numstore_pb2.SetNumRequest()):
        resp = randomFunction(key=randomKey, value=randomValue)
        print(resp.total)
    else:
        resp = randomFunction(key=randomKey)
        print(resp.value)

task()
thread_function()

# TEST SetNum
#resp = stub.SetNum(numstore_pb2.SetNumRequest(key="A", value=1))
#print(resp.total) # should be 1
#resp = stub.SetNum(numstore_pb2.SetNumRequest(key="B", value=10))
#print(resp.total) # should be 11
#resp = stub.SetNum(numstore_pb2.SetNumRequest(key="A", value=5))
#print(resp.total) # should be 15
#resp = stub.SetNum(numstore_pb2.SetNumRequest(key="B", value=0))
#print(resp.total) # should be 5

# TEST Fact
#resp = stub.Fact(numstore_pb2.FactRequest(key="A"))
#print(resp.value) # should be 120
#print(resp.hit) # should be false
