"""
GOAL: The goal of this exercise is to pass object IDs into remote functions to encode dependencies between tasks.

In this exercise, we construct a sequence of tasks, each of which depends on the previous, mimicking a data parallel
application. Within each sequence, tasks are executed serially, but multiple sequences of tasks can be executed in
parallel. You will use Ray to speed up the computation by parallelizing the sequences.
"""
import ray

ray.init()


@ray.remote
def test_function(x):
    return x


# Passing Data into Remote Functions
print("Passing Data into Remote Functions")
x1_id = test_function.remote(1)
print(ray.get(x1_id))

x2_id = test_function.remote([1, 2, 3])
print(ray.get(x2_id))

# Passing object IDs into Remote Functions
"""
However, object IDs can also be passed into remote functions. When the function is executed,
Ray will automatically substitute the underlying Python object that the object ID refers to.

In a sense, it's the same as calling ray.get on each argument that's passed in as an argument.
"""

print("Passing Object IDs into Remote Functions")
y1_id = test_function.remote(x1_id)
print(ray.get(y1_id))

y2_id = test_function.remote(x2_id)
print(ray.get(y2_id))
ray.shutdown()
