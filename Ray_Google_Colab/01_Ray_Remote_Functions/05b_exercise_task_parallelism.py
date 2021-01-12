"""
Exercise 2: To perform Task Parallelism between  4 helper tasks.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import time
import ray

ray.init(num_cpus=4, ignore_reinit_error=True)

# Sleep a little to improve the accuracy of the timing measurements used below,
# because some workers may still be starting up in the background.
time.sleep(2.0)

## Helper Functions - Converting to Remote Functions
@ray.remote
def load_data(filename):
    time.sleep(0.1)
    return np.ones((1000, 100))

@ray.remote
def normalize_data(data):
    time.sleep(0.1)
    return data - np.mean(data, axis=0)

@ray.remote
def extract_features(normalized_data):
    time.sleep(0.1)
    return np.hstack([normalized_data, normalized_data ** 2])

@ray.remote
def compute_loss(features):
    num_data, dim = features.shape
    time.sleep(0.1)
    return np.sum((np.dot(features, np.ones(dim)) - np.ones(num_data)) ** 2)

"""
To check whether the above helper functions have been made remote.
"""
# assert hasattr(load_data, 'remote'), 'load_data must be a remote function'
# assert hasattr(normalize_data, 'remote'), 'normalize_data must be a remote function'
# assert hasattr(extract_features, 'remote'), 'extract_features must be a remote function'
# assert hasattr(compute_loss, 'remote'), 'compute_loss must be a remote function'

start_time = time.time()
losses = []
for filename in ['file1', 'file2', 'file3', 'file4']:
    inner_start = time.time()

    data = load_data.remote(filename)
    normalized_data = normalize_data.remote(data)
    features = extract_features.remote(normalized_data)
    loss = compute_loss.remote(features)
    losses.append(loss)
    
    inner_end = time.time()
    
    if inner_end - inner_start >= 0.1:
        raise Exception('You may be calling ray.get inside of the for loop! '
                        'Doing this will prevent parallelism from being exposed. '
                        'Make sure to only call ray.get once outside of the for loop.')

print('The losses are {}.'.format(ray.get(losses)) + '\n')
loss = sum(ray.get(losses))

duration = time.time() - start_time

print('The loss is {}. This took {:.3f} seconds. Run the next cell to see '
      'if the exercise was done correctly.'.format(loss, duration))