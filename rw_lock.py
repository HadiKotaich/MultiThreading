"""
Imagine you have an application where you have multiple readers and a single writer. You are asked to design a lock which lets multiple readers read at the same time, but only one writer write at a time.
"""

from threading import Condition, Thread
import threading
import time

class RWLock():
    def __init__(self):
        self.condition = Condition()
        self.readers = 0
        self.writer = 0

    def acquire_read_lock(self):
        with self.condition:
            self.condition.wait_for(lambda: self.writer == 0)
            print(f"acquire_read_lock {threading.current_thread().name}")
            self.readers += 1
            self.condition.notify_all()

    def release_read_lock(self):
        with self.condition:
            print(f"release_read_lock {threading.current_thread().name}")
            self.readers -= 1
            self.condition.notify_all()

    def acquire_write_lock(self):
        with self.condition:
            self.condition.wait_for(lambda: self.readers == 0 and self.writer == 0)
            print(f"acquire_write_lock {threading.current_thread().name}")
            self.writer += 1
            self.condition.notify_all()
    
    def release_write_lock(self):
        with self.condition:
            print(f"release_write_lock {threading.current_thread().name}")
            self.writer -= 1
            self.condition.notify_all()

def test_read(lck):
    lck.acquire_read_lock()
    time.sleep(2)
    lck.release_read_lock()

def test_write(lck):
    lck.acquire_write_lock()
    time.sleep(2)
    lck.release_write_lock()

lck = RWLock()
t1 = Thread(target = test_read, args= (lck,), name = "1")
t2 = Thread(target = test_read, args= (lck,), name = "2")
t3 = Thread(target = test_write, args= (lck,), name = "3")
t4 = Thread(target = test_write, args= (lck,), name = "4")

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print("Done")