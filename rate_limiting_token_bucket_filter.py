from threading import Condition, Thread, Timer
import threading
from datetime import datetime
import time

class RateLimitingTokenBucketFilter:
    def __init__(self, n):
        self.n = n
        self.available = 0
        self.c = Condition()
        self.__add_token()

    def __add_token(self):
        with self.c:
            self.available = min(self.available + 1, self.n)
            self.c.notify_all()
            t = Timer(1, self.__add_token)
            t.start()
    def get_token(self):
        with self.c:
            self.c.wait_for(lambda: self.available > 0)
            self.available -= 1
            print(f"{threading.current_thread().name} got token at time {datetime.now()}")
            return True
"""
     For add token consider this instead:
     
     def __init__(self, maxTokens):
        self.MAX_TOKENS = int(maxTokens)
        self.possibleTokens  = int(0)
        self.ONE_SECOND = int(1)
        self.cond = Condition()
        dt = Thread(target = self.daemonThread);
        dt.setDaemon(True);
        dt.start();
    
        
    def daemonThread(self):
        while True:
            self.cond.acquire()
            if self.possibleTokens < self.MAX_TOKENS:
                self.possibleTokens = self.possibleTokens + 1;
            self.cond.notify() 
            self.cond.release()
            
            time.sleep(self.ONE_SECOND);
     
     Consider using a factory as well, not advisable to have thread creation in constructor.
     
     
class TokenBucketFilterFactory:

    @staticmethod
    def makeTokenBucketFilter(capacity):
        tbf = MultithreadedTokenBucketFilter(capacity)
        tbf.initialize();
        return tbf;

class MultithreadedTokenBucketFilter:
    def __init__(self, maxTokens):
        self.MAX_TOKENS = int(maxTokens)
        self.possibleTokens  = int(0)
        self.ONE_SECOND = int(1)
        self.cond = Condition()

    def initialize(self):
        dt = Thread(target = self.daemonThread);
        dt.setDaemon(True);
        dt.start();
     
"""

x = RateLimitingTokenBucketFilter(5)
time.sleep(5)
ts = []
for i in range(10):
    t1 = Thread(target = x.get_token, name=f"T_{i}" , args = ())
    t1.start()
    ts.append(t1)

for t in ts:
    t.join()

print("done")
class RateLimitingTokenBucketFilter2:
    def __init__(self, n):
        self.n = n
        self.available = 0
        self.last = datetime.now().timestamp()
        self.lock = Lock()

    def get_token(self):
        with self.lock:
            now = datetime.now().timestamp()
            self.available = min(self.n, self.available + int(now - self.last))
            if self.available == 0:
                time.sleep(1)
                now = datetime.now().timestamp()
                self.available = min(self.n, self.available + int(now - self.last))
            self.available -= 1
            self.last = now
            print(f"{threading.current_thread().name} got token at time {datetime.now()}")
            return True