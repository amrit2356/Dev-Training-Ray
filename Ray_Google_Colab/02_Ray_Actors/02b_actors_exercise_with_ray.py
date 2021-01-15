"""
Exercise 4: Make the Foo class an actor class |using the @ray.remote decorator.
(This code is with Ray Implementation)
"""
import ray
import time

ray.init()

@ray.remote
class Foo(object):
    def __init__(self):
        self.counter = 0

    def reset(self):
        self.counter = 0

    def increment(self):
        time.sleep(0.5)
        self.counter += 1
        return self.counter

f1 = Foo.remote()
f2 = Foo.remote()

start_time = time.time()

# Reset the actor state so that we can run this cell multiple times without
# changing the results.
ray.get(f1.reset.remote())
ray.get(f2.reset.remote())

# We want to parallelize this code. However, it is not straightforward to
# make "increment" a remote function, because state is shared (the value of
# "self.counter") between subsequent calls to "increment". In this case, it
# makes sense to use actors.
results = []
for _ in range(5):
    results.append(f1.increment.remote())
    results.append(f2.increment.remote())

results = ray.get(results)
duration = time.time() - start_time

assert not any([isinstance(result, ray.ObjectID) for result in results]), 'Looks like "results" is {}. You may have forgotten to call ray.get.'.format(results)
print('Duration of the Exercise without Ray: {:.3f}'.format(duration))

assert results == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

assert duration < 3, ('The experiments ran in {:.3f} seconds. This is too '
                      'slow.'.format(duration))
assert duration > 2.5, ('The experiments ran in {:.3f} seconds. This is too '
                        'fast.'.format(duration))

print('Success! The example took {:.3f} seconds.'.format(duration))


ray.shutdown()