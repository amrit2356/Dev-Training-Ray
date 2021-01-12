"""
Exercise 2: To perform Task Parallelism between  4 helper tasks.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import time

## Helper Functions
def load_data(filename):
    time.sleep(0.1)
    return np.ones((1000, 100))

def normalize_data(data):
    time.sleep(0.1)
    return data - np.mean(data, axis=0)

def extract_features(normalized_data):
    time.sleep(0.1)
    return np.hstack([normalized_data, normalized_data ** 2])

def compute_loss(features):
    num_data, dim = features.shape
    time.sleep(0.1)
    return np.sum((np.dot(features, np.ones(dim)) - np.ones(num_data)) ** 2)


start_time = time.time()
losses = []
for filename in ['file1', 'file2', 'file3', 'file4']:
    inner_start = time.time()

    data = load_data(filename)
    normalized_data = normalize_data(data)
    features = extract_features(normalized_data)
    loss = compute_loss(features)
    losses.append(loss)
    
    inner_end = time.time()

print('The losses are {}.'.format(losses) + '\n')
loss = sum(losses)

duration = time.time() - start_time

print('The loss is {}. This took {:.3f} seconds. Run the next cell to see '
      'if the exercise was done correctly.'.format(loss, duration))