"""
Implementation of Ray Actors in Ray
"""
import ray
"""
Although remote functions are useful for parallelizing stateless computations, 
sometimes your workload requires maintaining state across invocations. Some examples 
might be a simple counter, a neural network during training, or a simulator environment. 

If using remote functions, you would have to pass this state into each function invocation 
and return the updated state when it finishes.

However, Ray comes with a stateful abstraction for these situations: remote actors. An actor 
is a lot like a Python object - it is initialized with an __init__ function (that has the same 
features has remote tasks), and can contain internal state that is accessed and mutated by 
remote method calls. 

Remote method calls will be executed one at a time on each actor, so there's no need to worry 
about race conditions on the actor's state. To achieve more parallelism, multiple actors can 
be created.
"""
ray.init()


### This is an Actor(A Python class decorated with ray.remote)
@ray.remote
class Actor:
    def __init__(self, x):
        self.x = x
 
    def set(self, x):
        self.x = x
 
    def get(self):
        return self.x

# Instantiation of Actor
actor_object = Actor.remote(1)

# Method Invocation of actor.

print(actor_object.set.remote(2))

#Return Values 
"""Use ray.get() to get actual result from the methods. Otherwise output will be an obj. reference.
print(ray.get(actor_object.get.remote()))


ray.shutdown()