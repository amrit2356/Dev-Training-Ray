"""
Exercise 1: To bring down a process time execution from 4 secs to 1 sec.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ray
import time

time.sleep(2)
# Slowfunction: takes lot of time to process a task


def slow_function(i):
    time.sleep(1)
    return i


start_time = time.time()

results = []
for i in range(4):
    results.append(slow_function(i))

duration = time.time() - start_time
print('Executing the for loop took {:.3f} seconds.'.format(duration))
print('The results are:', results)
print('Run the next cell to check if the exercise was performed correctly.')


# FastFunction: Faster than the above function
ray.init(num_cpus=4, ignore_reinit_error=True)


@ray.remote
def fast_function(i):
    time.sleep(1)
    return i


start_time = time.time()
results = []
for i in range(4):
    results.append(fast_function.remote(i))
results = ray.get(results)
duration = time.time() - start_time
print('Executing the for loop took {:.3f} seconds.'.format(duration))
print('The results are:', results)
print('Run the next cell to check if the exercise was performed correctly.')
ray.shutdown()

assert results == [0, 1, 2, 3], 'Did you remember to call ray.get?'
assert duration < 1.1, ('The loop took {:.3f} seconds. This is too slow.'
                        .format(duration))
assert duration > 1, ('The loop took {:.3f} seconds. This is too fast.'
                      .format(duration))

print('Success! The example took {:.3f} seconds.'.format(duration))
