import socket
import json


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = ""
        self.port = 9501
        self.addr = (self.host, self.port)
        self.client.bind(self.addr)

    def recv(self, conn):
        try:
            header_size = conn.recv(8)
            header_size = int.from_bytes(header_size, "little")
            header = conn.recv(header_size)
            if not header:
                raise(BrokenPipeError)
                return
            header = header.decode("utf-8")
            header = json.loads(header)

            data = conn.recv(header["message_length"])
            if header["type"] == "str":
                data = data.decode("utf-8")
            return data
        except BrokenPipeError:
            raise(BrokenPipeError)
        except Exeption:
            return "disconnected"

    def send(self, data_type, data, user):
        try:
            conn = user.conn
            if data_type == "str":
                array = str.encode(data)
            else:
                return
            header = {"type": data_type, "message_length": len(array), "request": False}
            if header["message_length"] == 0:
                header["message_length"] = 1
                array = b'-'
            header_array = json.dumps(header)
            header_array = header_array.encode("utf-8")
            header_length = len(header_array)
            header_length = int.to_bytes(header_length, 8, "little")
            conn.sendall(header_length)
            conn.sendall(header_array)
            conn.sendall(array)
        except Exception as E:
            print(E)
    def request(self, data_type, data, user, force_strings=True):
        try:
            conn = user.conn
            if data_type == "str":
                array = str.encode(data)
            else:
                return
            header = {"type": data_type, "message_length": len(array), "request": True}
            header_array = json.dumps(header)
            header_array = header_array.encode("utf-8")
            header_length = len(header_array)
            header_length = int.to_bytes(header_length, 8, "little")
            conn.sendall(header_length)
            conn.sendall(header_array)
            conn.sendall(array)
            if force_strings:
                reply = self.recv(conn)
                if type(reply) != str:
                    print(f"{user.name} SEEMS TO USE A MODIFIED CLIENT")
                reply = f"{reply}"
            else:
                reply = self.recv(conn)
            return reply
        except:
            return "disconnected"
