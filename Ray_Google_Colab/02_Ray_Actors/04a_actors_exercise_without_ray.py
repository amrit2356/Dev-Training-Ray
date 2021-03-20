from __future__ import absolute_import, division, print_function

import time
from collections import defaultdict

import ray

"""
Exercise 5: Turn this LoggingActor class into an actor class.

"""

ray.init(ignore_reinit_error=True)


@ray.remote
class LoggingActor(object):
    def __init__(self):
        self.logs = defaultdict(lambda: [])

    def log(self, index, message):
        self.logs[index].append(message)

    def get_logs(self):
        return dict(self.logs)


assert hasattr(LoggingActor, 'remote'), ('You need to turn LoggingActor into an '
                                         'actor (by using the ray.remote keyword).')

logging_actor = LoggingActor.remote()


@ray.remote
def run_experiment(experiment_index, logging_actor):
    for i in range(60):
        time.sleep(1)
        # Push a logging message to the actor.
        logging_actor.log.remote(experiment_index, 'On iteration {}'.format(i))


experiment_ids = []
for i in range(3):
    experiment_ids.append(run_experiment.remote(i, logging_actor))


logs = ray.get(logging_actor.get_logs.remote())
exp_id = ray.get(experiment_ids)
assert isinstance(logs, dict), ("Make sure that you dispatch tasks to the "
                                "actor using the .remote keyword and get the results using ray.get.")
print(experiment_ids)

print(logs)
ray.shutdown()
