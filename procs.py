import concurrent.futures
import math
import time
import sys

if len(sys.argv) > 1:
    num_procs = int(sys.argv[1])
else:
    num_procs = 1

primes = [112272535095293,112582705942171,112272535095293,115280095190773,115797848077099,1099726899285419] * 10

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

with concurrent.futures.ProcessPoolExecutor(max_workers=num_procs) as executor:
    start = time.time()
    for number, prime in zip(primes, executor.map(is_prime, primes)):
        print('%d is prime: %s' % (number, prime))
    end = time.time()
    print('total execution time = %.6f' % (end - start)) 
