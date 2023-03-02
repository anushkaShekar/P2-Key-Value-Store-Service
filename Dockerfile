FROM ubuntu:22.10
RUN apt-get update
RUN apt-get install -y wget curl openjdk-11-jdk python3 python3-pip net-tools lsof nano
RUN python3 -m pip install --upgrade pip
RUN pip install grpcio grpcio-tools
COPY ["server.py", "/server.py"]
COPY ["numstore.proto", "/numstore.proto"]
COPY ["numstore_pb2.py", "/numstore_pb2.py"]
COPY ["numstore_pb2_grpc.py", "/numstore_pb2_grpc.py"]
CMD ["python3", "/server.py", "--ip=0.0.0.0.", "--port=5440", "--allow-root"]



