import socket


def ensure_kafka_connectivity(kafka_config):
    """
    Helper method just to make sure our Kafka broker host:port is open, to avoid starting the spider if not
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr, port = tuple(kafka_config['bootstrap.servers'].split(':'))
    if sock.connect_ex((addr, int(port))) != 0:
        raise Exception(f"cannot connect to kafka at {addr}:{port}, is the docker-compose running?")
