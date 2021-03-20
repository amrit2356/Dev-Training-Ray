import ray
from ray_queue_1 import queue1

def main():
    ray.init()
    q1 = queue1.remote()
    # q2 = queue2.remote()
    value = 'Amrit'
    a1 = ray.put(value)
    q1.read.remote(a1)
    q1.start.remote()
    # return_value = ray.get(q1.write.remote())
    # print(return_value)
    del a1
    ray.shutdown()

if __name__ == "__main__":
    main()
