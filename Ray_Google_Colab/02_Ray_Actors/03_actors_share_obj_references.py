"""
Sharing References to an Actor:
GOAL: The goal of this exercise is to show how to pass references to actors to remote functions and methods.

Sometimes, we may want to have multiple remote tasks that invoke methods on the same actor. For example, we 
may have a single actor that records logging information for a group of tasks and allows other tasks to query 
the logs. 

We can achieve this by passing a handle to the actor (the object returned from calling Actor.remote()) as an 
argument to the tasks.
"""
import ray

ray.init()

#Creation of Actor
@ray.remote
class Actor(object):
    def __init__(self):
        self.counter = 0
    
    def increment(self):
        self.counter += 1
    
    def get_counter(self):
        return self.counter
 
# Create the actor
actor_obj_1 = Actor.remote()

# We can invoke a method on the actor and wait for its result.
@ray.remote
def f(actor):
    actor.increment.remote()
    actor.increment.remote()
    return ray.get(actor.get_counter.remote())


print(ray.get(f.remote(actor_obj_1)))

ray.shutdown()

