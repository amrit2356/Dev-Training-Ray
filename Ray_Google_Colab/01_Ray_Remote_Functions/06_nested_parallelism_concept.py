"""
Implementation of Nested Parallelism in Ray

"""
import ray

ray.init()

@ray.remote
def function_1():
    return 1

@ray.remote
def nesting_function_without_ray_get():
    # Call f 4 times and return the resulting object IDs.
    results = []
    for _ in range(4):
        results.append(function_1.remote())
    return results

# Printing the 4 Object IDs coming from the nesting function.
print(ray.get(nesting_function_without_ray_get.remote()))


@ray.remote
def nesting_func_with_ray_get():
    # Call f 4 times, block until those 4 tasks finish,
    # retrieve the results, and return the values.
    results = []
    for _ in range(4):
        results.append(function_1.remote())
    return ray.get(results)

print(ray.get(nesting_func_with_ray_get.remote()))
# Printing the results, where the Function returns the proper out while using ray.get()

ray.shutdown()
