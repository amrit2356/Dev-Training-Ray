"""
Exercise 3: Nested Parallelism for 3 Tasks
GOAL: The goal of this exercise is to show how to create nested tasks by calling a remote function inside of another remote function.

In this exercise, you will implement the structure of a parallel hyperparameter sweep which trains a number of models in parallel. 
Each model will be trained using parallel gradient computations.

Turn compute_gradient and train_model into remote functions so that they can be executed in parallel. 
Inside of train_model, do the calls to compute_gradient in parallel and fetch the results using ray.get.
"""
import ray
import time 


ray.init()

@ray.remote
def compute_gradient(data, current_model):
    time.sleep(0.03)
    return 1

@ray.remote
def train_model(hyperparameters):
    current_model = 0
    # Iteratively improve the current model. This outer loop cannot be parallelized.
    for _ in range(10):
        # EXERCISE: Parallelize computing the gradients below. Note that we still need
        # to get all of the results in order to compute the updated model (by taking
        # the sum), so it's ok to call ray.get() inside of the loop here.
        gradients = []
        for j in range(2):
            gradients.append(compute_gradient.remote(j, current_model))
        gradients = ray.get(gradients)
        current_model += sum(gradients)

    return current_model

assert hasattr(compute_gradient, 'remote'), 'compute_gradient must be a remote function'
assert hasattr(train_model, 'remote'), 'train_model must be a remote function'

# Sleep a little to improve the accuracy of the timing measurements below.
time.sleep(2.0)
start_time = time.time()

# Run some hyperparaameter experiments.
results = []
for hyperparameters in [{'learning_rate': 1e-1, 'batch_size': 100},
                        {'learning_rate': 1e-2, 'batch_size': 100},
                        {'learning_rate': 1e-3, 'batch_size': 100}]:
    results.append(train_model.remote(hyperparameters))
results = ray.get(results)

# EXERCISE: Once you've turned "results" into a list of Ray ObjectIDs
# by calling train_model.remote, you will need to turn "results" back
# into a list of integers, e.g., by doing "results = ray.get(results)".

end_time = time.time()
duration = end_time - start_time

print("Duration for Running the Program:{:.3f}".format(duration))

assert results == [20, 20, 20]
assert duration < 0.5, ('The experiments ran in {:.3f} seconds. This is too '
                         'slow.'.format(duration))
assert duration > 0.3, ('The experiments ran in {:.3f} seconds. This is too '
                        'fast.'.format(duration))

print('Success! The example took {:.3f} seconds.'.format(duration))

ray.shutdown()