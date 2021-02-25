"""
Basic Implementation of Ray
"""
import ray


# Initialization of Ray
ray.init()

"""
There are a few key differences between the original function and the decorated one:

    Invocation: The regular version is called with function(), whereas the remote
    version is called with remote_function.remote().

    Return values: function() executes synchronously and returns the result of the function
    (1), whereas remote_function immediately returns an ObjectID (a future) and then executes the
    task in the background on a separate worker process. The result of the future can be obtained
    by calling ray.get on the ObjectID.
"""


# Creation of Normal Python Function
def function():
    return 1

# Creation of Ray Remote function


@ray.remote
def remote_function():
    return 1


# Result

# Printing Normal Function
print(function())

# Accessing the Object Reference of Ray Remote Function
print(remote_function.remote())

# Accessing the future value of Ray Remote Function using the ray.get()
print(ray.get(remote_function.remote()))

# Shutting down Ray
ray.shutdown()
