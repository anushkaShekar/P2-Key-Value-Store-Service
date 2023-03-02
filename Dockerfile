FROM ubuntu:22.10
RUN apt-get update
RUN apt-get install -y python3 python3-pip curl lsof
CMD ["python3", "server.py", "--ip=0.0.0.0.", "--port=5440", "--allow-root"]
#CMD ["ls"]
#CMD ["pwd"]
#CMD ["cd /home"]


