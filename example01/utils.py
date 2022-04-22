from eventsourcing.system import SingleThreadedRunner, MultiThreadedRunner, NewMultiThreadedRunner


def set_runner(system):
    if hasattr(system, 'runner'):
        runner = getattr(system, 'runner')
    else:
        runner = SingleThreadedRunner(system)
        setattr(system, 'runner', runner)
    if not system.runner.is_started:
        system.runner.start()
    return system.runner


def get_runner(system):
    return system.runner


#!/usr/bin/env python2
"""Demonstration of a Python logging handler that creates a separate output
file for each stream. The key thing here is the class MultiHandler. It picks
the file name based on the thread name; could use anything in threading.local()
"""

import threading, logging, time, random, os

# Global object we log to; the handler will work with any log message
_L = logging.getLogger("demo")
"""
Link to source code:
https://gist.github.com/NelsonMinar/74d94f8bcb78fae150e3
"""


def set_logger(system):
    logger = logging.getLogger("root")
    ### Set up basic stderr logging; this is nothing fancy.
    log_format = '%(asctime)s %(relativeCreated)6.1f %(threadName)12s: %(levelname)s %(module)s:%(lineno)-4d %(message)s'
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(stderr_handler)

    ### Set up a logger that creates one file per thread
    file_handler = logging.FileHandler('./logs/example01.log')
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    ### Set default log level, log a message
    logger.setLevel(logging.DEBUG)
    logger.info("Run initiated")

    ### Create some tasks and run them with Thread names
    #tasks = (("red", Task()), ("green", Task()), ("blue", Task()))
    #for name, task in tasks:
    #    thread = threading.Thread(target=task.run, name=name)
    #    thread.start()
    setattr(system, "logger", logger)
    return logger


def get_logger(system):
    return system.logger