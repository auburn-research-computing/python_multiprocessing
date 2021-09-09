import sys
import threading
import concurrent.futures
import urllib.request
import time

if len(sys.argv) > 1:
    num_threads = int(sys.argv[1])
else:
   num_threads = 1
 
    
# define a list of web addresses to use in i\o simulation

urls = ['http://hpc.auburn.edu',
        'http://python.org'
       ] * 10


# function: load_url(string, integer)
# send a request using the provided url and read the response

def load_url(url, timeout = 60):
    print('thread %s entered load_url()' % (threading.current_thread().name))
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# main code: demonstrate thread based parallelism using Python concurrent.futures
# 1. create an "executor" to manage the allocation of threads 
# 2. call submit() to spawn a thread for each url in our array
# 3. upon completion of each thread print the result and metrics 

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor: # 1
    start_loop = time.time()
    threads = { executor.submit(load_url, url): url for url in urls } # 2
    for thread in concurrent.futures.as_completed(threads): # 3
        start_request = time.time()
        url = threads[thread]
        try:
            data = thread.result()
            end_request = time.time()
        except Exception as e:
            print('%24s generated an exception: %s' % (url, e))
        else:
            print('%24s response was %d bytes in %.10f seconds' % (url, len(data), (end_request - start_request)))
    end_loop = time.time()
    print('total execution time: %.2gs' % (end_loop - start_loop))
