"""
Design and implement a thread-safe class that allows registration of callback methods that are executed after a user specified time interval in seconds has elapsed.
"""
from threading import Timer

class CallbacksRegister():
    def __init__(self):
        self.timers = []

    def registerCallback(self, callback, time):
        t = Timer(time, callback)
        t.start()
        self.timers.append(t)

    def join(self):
        for t in self.timers:
            t.join()

cb = CallbacksRegister()
cb.registerCallback(lambda: print("callback 5"), 5)
cb.registerCallback(lambda: print("callback 3"), 3)
cb.registerCallback(lambda: print("callback 10"), 10)
cb.registerCallback(lambda: print("callback 1"), 1)
cb.registerCallback(lambda: print("callback 7"), 7)

cb.join()

print("done")

"""
Design and implement a thread-safe class that allows registration of callback methods that are executed after a user specified time interval in seconds has elapsed.
"""

import time
from threading import Thread, Lock

class CallbacksRegister():
    def __init__(self):
        self.timers = []
        self.lock = Lock()

    def defer(self, callback, delay):
        time.sleep(delay)
        callback()

    def registerCallback(self, callback, delay):
        t = Thread(target = self.defer, args= (callback, delay))
        t.start()
        with self.lock:
            self.timers.append(t)

    def join(self):
        for t in self.timers:
            t.join()

cb = CallbacksRegister()
cb.registerCallback(lambda: print("callback 5"), 5)
cb.registerCallback(lambda: print("callback 3"), 3)
cb.registerCallback(lambda: print("callback 10"), 10)
cb.registerCallback(lambda: print("callback 1"), 1)
cb.registerCallback(lambda: print("callback 7"), 7)

cb.join()

print("done")