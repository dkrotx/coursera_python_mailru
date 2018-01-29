import time
import socket

class ClientError(Exception):
    pass

class Client:
    def __init__(self, addr, port, timeout=None):
        self.conn = socket.create_connection((addr, port), timeout)

    def __read_answer(self) -> str:
        answ = b''
        
        while True:
            data = self.conn.recv(1024)
            if not data:
                raise ClientError("Server closed connection without answer")
            
            answ += data
            if answ.endswith(b"\n\n"):
                break

        return answ[:-2].decode('utf-8') # rid the '\n\n' - that's a transport marker

    def __send_and_read_answer(self, msg):
        self.conn.sendall(msg.encode('utf-8'))
        answ = self.__read_answer()
        if answ.startswith('error\n'):
            raise ClientError(answ.split('\n')[1])
        
        if not answ.startswith('ok'):
            raise ClientError('Wrong answer format')

        start = 2
        if len(answ) > start and answ[start] == '\n':
            start += 1
        return answ[start:]

    def put(self, mname, mval, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        self.__send_and_read_answer(f"put {mname} {mval} {timestamp}\n")
        

    def get(self, expr):
        metrics = self.__send_and_read_answer(f"get {expr}\n")

        res = {}
        for m in filter(lambda x: x, metrics.split('\n')):
            mname, mval, timestamp = m.split()
            if mname not in res:
                res[mname] = []
            
            res[mname].append((int(timestamp), float(mval)))

        for k,v in res.items():
            v.sort()

        return res