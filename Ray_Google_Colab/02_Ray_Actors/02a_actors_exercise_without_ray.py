"""
Exercise 4: Make the Foo class an actor class |using the @ray.remote decorator.
(This code is without Ray Implementation)
"""

import time
class Foo(object):
    def __init__(self):
        self.counter = 0

    def reset(self):
        self.counter = 0

    def increment(self):
        time.sleep(0.5)
        self.counter += 1
        return self.counter

f1 = Foo()
f2 = Foo()

start_time = time.time()

# Reset the actor state so that we can run this cell multiple times without
# changing the results.
f1.reset()
f2.reset()

# We want to parallelize this code. However, it is not straightforward to
# make "increment" a remote function, because state is shared (the value of
# "self.counter") between subsequent calls to "increment". In this case, it
# makes sense to use actors.
results = []
for _ in range(5):
    results.append(f1.increment())
    results.append(f2.increment())

duration = time.time() - start_time

print('Duration of the Exercise without Ray: {:.3f}'.format(duration))