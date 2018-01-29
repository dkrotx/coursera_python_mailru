from collections import defaultdict
from operator import itemgetter
import asyncio

class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class MetricsStorage:
    def __init__(self):
        self.metrics = defaultdict(dict)
    
    def put(self, metric, value, timestamp):
        self.metrics[metric][timestamp] = value

    def get(self, expr):
        answ = []
        if expr == '*':
            for m, tv in self.metrics.items():
                for t, v in tv.items():
                    answ.append((m, v, t))

        if expr in self.metrics:
            for t, v in self.metrics[expr].items():
                answ.append((expr, v, t))

        return sorted(answ, key=itemgetter(2))

class BadInputFormat(Exception):
    pass

class MetricsServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def _extract_put_args(self, args):
        try:
            metric = args[1]
            value = float(args[2])
            timestamp = int(args[3])
            return metric, value, timestamp
        except Exception:
            raise BadInputFormat('put expects "metric(str) value(float) timestamp(int)')

    def _extract_get_arg(self, args):
        try:
            return args[1]
        except IndexError:
            raise BadInputFormat('get expects expression of metrics')

    def _format_get_result(self, arr):
        res = ''
        for metric, value, timestamp in arr:
            res += f'\n{metric} {value} {timestamp}' # \n divide elements

        return res

    def handle_request(self, line: str):
        args = line.split()
        cmd = args[0]
        storage = MetricsStorage.Instance()

        if cmd == 'put':
            storage.put(*self._extract_put_args(args))
            return ''
        elif cmd == 'get':
            answ = storage.get(self._extract_get_arg(args))
            return self._format_get_result(answ)
        
        raise BadInputFormat(f'Unknown command "{cmd}"')

    def data_received(self, data):
        answer = ''
        try:
            answer = 'ok' + self.handle_request(data.decode())
        except BadInputFormat as e:
            answer = 'error\n' + str(e)
        
        answer += '\n\n' # message protocol terminator
        self.transport.write(answer.encode())

def run_server(addr, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        MetricsServer,
        addr, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server('127.0.0.1', 8888)
