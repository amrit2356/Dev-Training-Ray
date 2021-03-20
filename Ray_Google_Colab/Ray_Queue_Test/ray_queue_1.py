import ray
from queue import Queue
from threading import Thread
from ray_queue_2 import queue2

@ray.remote
class queue1:

    complete = False

    def __init__(self, queue_size=32):
        self.q = Queue(maxsize=queue_size)
        self.queue_second = queue2.remote()

    def start(self):
        t = Thread(target=self.__read_values, args=())
        t.daemon = True
        t.start()

    def __read_values(self):
        if self.q.qsize() > 0:
            value_q1 = self.q.get()
        print("Entering into Queue 1: {}".format(value_q1))
        self.queue_second.read.remote(value_q1)
        self.queue_second.start.remote()

    def read(self, value):
        if not self.q.full():
            self.q.put(value)

    def write(self):
        return self.q.get()
