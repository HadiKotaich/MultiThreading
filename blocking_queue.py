from threading import Condition, Thread
from queue import Queue
import time

class blockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.condition = Condition()
        self.q = Queue()

    def enqueue(self, e):
        with self.condition:
            self.condition.wait_for(lambda: self.q.qsize() < self.capacity)
            self.q.put(e)
            self.condition.notify_all()
            print(f"enqueued {e}")
    def dequeue(self):
        with self.condition:
            self.condition.wait_for(lambda: self.q.qsize() > 0)
            ans = self.q.get()
            self.condition.notify_all()
            print(f"dequeued {ans}")
            return ans

q = blockingQueue(5)

for i in range(5):
    q.enqueue(i)

t1 = Thread(target = q.enqueue, args = (6,))
t2 = Thread(target = q.enqueue, args = (7,))

t1.start()
t2.start()

time.sleep(3)

t3 = Thread(target = q.dequeue, args = ())
t4 = Thread(target = q.dequeue, args = ())

t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

for i in range(5):
    q.dequeue()

t5 = Thread(target = q.dequeue, args = ())
t5.start()
time.sleep(3)

t6 = Thread(target = q.enqueue, args = (8,))
t6.start()

t5.join()
t6.join()