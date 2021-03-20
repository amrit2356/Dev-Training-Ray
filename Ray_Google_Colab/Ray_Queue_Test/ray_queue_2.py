import ray
from queue import Queue
from threading import Thread

@ray.remote
class queue2:

    def __init__(self, queue_size=32):
        self.q = Queue(maxsize=queue_size)

    def start(self):
        t = Thread(target=self.__read_values, args=())
        t.daemon = True
        t.start()

    def __read_values(self):
        value_q2 = None
        if self.q.qsize() > 0:
            value_q2 = self.q.get()
        print("Entering into Queue 2: {}".format(value_q2))

    def read(self, value):
        if not self.q.full():
            self.q.put(value)
