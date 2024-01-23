#!/usr/bin/env python3

# This example shows how to install a library of functions once
# as a LibraryTask, and then invoke that library remotely by
# using FunctionCall tasks.

import ndcctools.taskvine as vine
import argparse
import math

import json

# The library will consist of the following three functions:

def cube(x):
    # whenever using FromImport statments, put them inside of functions
    from random import uniform
    from time import sleep as time_sleep

    random_delay = uniform(0.00001, 0.0001)
    time_sleep(random_delay)

    return math.pow(x, 3)

def divide(dividend, divisor):
    # straightfoward usage of preamble import statements
    return dividend / math.sqrt(divisor)

def double(x):
    import math as m
    # use alias inside of functions
    return m.prod([x, 2])

def retrieve_fn(task):
    future_tracker = vine.FutureTaskTracker(task)
    return future_tracker


def main():

    executor = vine.Executor(port=9125, factory=False)

    print(f"TaskVine manager listening on port {executor.manager.port}")

    print("Creating library from packages and functions...")

    import_modules = [math]
    libtask = executor.manager.create_library_from_functions('test-library', divide, retrieve_fn, import_modules=import_modules, add_env=False)
    

    executor.manager.install_library(libtask)

    print("Submitting function call tasks...")

    t1 = executor.future_funcall('test-library', 'divide', 8, 2**2)
    executor.submit(t1)

    t2 = executor.future_funcall('test-library', 'divide', t1.output, t1.output)
    executor.submit(t2)

    t3 = executor.future_funcall('test-library', 'divide', t2.output, t1.output)
    executor.submit(t3)

    print(f"t1 output is {t1.output}")
    print(f"t2 output is: {t2.output}")
    print(f"t2 output is: {t3.output}")

if __name__ == '__main__':
    main()


# vim: set sts=4 sw=4 ts=4 expandtab ft=python:
