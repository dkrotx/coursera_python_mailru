from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
import math

def calc_max_prime(num):
    primes = [2]

    for x in range(3, num):
        max_check = int(math.sqrt(x)) + 1
        prime = True
        for p in primes:
            if p > max_check:
                break
            if x % p == 0:
                prime = False
                break
        if prime:
            primes.append(x)

    return primes[-1]


with ThreadPoolExecutor(max_workers=2) as pool:
    results = [pool.submit(calc_max_prime, 10**6) for x in range(6)]

    for f in as_completed(results):
        print("Result: {}".format(f.result()))

Thread()