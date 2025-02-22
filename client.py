import sys
import grpc
import threading, time
import numpy as np
import random, string
import numstore_pb2_grpc
import numstore_pb2

port = "54321"
addr = f"127.0.0.1:{port}"
channel = grpc.insecure_channel(addr)
stub = numstore_pb2_grpc.NumStoreStub(channel)

latencies = []
hits = []
hit_rate = 0

key_list = []
for i in range(100):
    randomLetter = random.choice(string.ascii_uppercase)
    key_list.append(randomLetter)

def task():
    for i in range(8):
        t = threading.Thread(target=thread_function)
        t.start()
        t.join()

    if len(hits) != 0:
        global hit_rate
        hit_rate = sum(hits) / len(hits)
    print("Cache hit rate: ", hit_rate)
    print("p50 response time: ", np.quantile(latencies, 0.5))
    print("p90 response time: ", np.quantile(latencies, 0.99))

def thread_function():
    global key_list

    for i in range(100):
        randomKey = random.choice(key_list)
        randomValue = random.randint(1, 15)
        randomOperation = random.randint(0, 1)
        
        if randomOperation == 0:
            start = time.time()
            stub.SetNum(numstore_pb2.SetNumRequest(key=randomKey, value=randomValue))
            end = time.time()
            global latencies
            latencies.append(end - start)
        else:
            start = time.time()
            resp = stub.Fact(numstore_pb2.FactRequest(key=randomKey))
            end = time.time()
            latencies.append(end-start)

            if resp.hit == True:
                global hits
                hits.append(1)
            else:
                hits.append(0)

task()
