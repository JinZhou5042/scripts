import ndcctools.taskvine as vine
from tqdm import tqdm
import gc
import time
import resource
import sys
import cloudpickle
import numpy as np
import math
import numpy
import matplotlib.pyplot as plt


def multiply_random_matrices(size=1000):
    import numpy
    matrix1 = numpy.random.rand(size, size)
    matrix2 = numpy.random.rand(size, size)

    return numpy.dot(matrix1, matrix2)


def main():

    q = vine.Manager(port=9123)
    q.set_name("test_manager")

    libtask = q.create_library_from_functions('test-library', multiply_random_matrices)
    libtask.set_cores(4)
    libtask.set_function_slots(4)
    q.install_library(libtask)


    tasks = 256
    for _ in range(0, tasks):
        s_task = vine.FunctionCall('test-library', 'multiply_random_matrices', 1000)
        q.submit(s_task)

    print("Waiting for results...")
    pbar = tqdm(total=tasks)

    time_start = time.time()

    while not q.empty():
        t = q.wait(5)
        if t:
            t.output
            pbar.update(1)

    pbar.close()

    print(f"tasks completed: {tasks*2}, time used: {(time.time() - time_start):.4}s")


if __name__ == '__main__':
    main()
