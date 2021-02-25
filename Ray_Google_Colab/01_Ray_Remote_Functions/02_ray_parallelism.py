import ray
"""
Parallelism with Ray
"""
# Creation of Normal Python Function
def function():
    return 1

# This code adds 4 values synchronously(one by one).
ray.init()
result = 0
for _ in range(4):
    result += function()
assert result == 4
print(result)


# Creation of Ray Remote function
@ray.remote
def remote_function():
    return 1

# using Remote function to access all the values simultaneously.
results = []
for _ in range(4):
    results.append(remote_function.remote())
assert sum(ray.get(results)) == 4
print(sum(ray.get(results)))
ray.shutdown()
