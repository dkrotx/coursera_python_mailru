from multiprocessing import Process

def fn(name):
    print("Hello: {}".format(name))

p = Process(target=fn, args=("Jan",))
p.start()
p.join()
