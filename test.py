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

def gen_random_list(size=10000):
    import random
    random_list = [random.randint(1, 100) for _ in range(size)]
    return random_list

def multiply_random_matrices(size):
    matrix1 = numpy.random.rand(size, size)
    matrix2 = numpy.random.rand(size, size)

    return numpy.dot(matrix1, matrix2)

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(np.floor(np.log(size_bytes) / np.log(1024)))
    p = np.power(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def main():

    q = vine.Manager(port=9123)
    q.set_name("test_manager")

    libtask = q.create_library_from_functions('test-library', gen_random_list, multiply_random_matrices, import_modules=[numpy])
    q.install_library(libtask)

    tasks = 100
    for _ in range(0, tasks):
        s_task = vine.FunctionCall('test-library', 'multiply_random_matrices', 3000)
        q.submit(s_task)

    print("Waiting for results...")
    pbar = tqdm(total=tasks)
    time_start = time.time()

    id = 0
    x = []
    y = []
    
    while not q.empty():
        t = q.wait(0)
        if t:
            o = t.output
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            id += 1
            x.append(id)
            y.append(memory_usage)
            pbar.update(1)

    plt.plot(x, y)
    plt.title("memory usage")
    plt.xlabel("tasks completed")
    plt.ylabel("memory used (MB)")
    plt.savefig('memory_usage.png')

    pbar.close()
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory_usage = convert_size(memory_usage)

    print(f"tasks completed: {tasks}, time used: {(time.time() - time_start):.4}s, memory consumed: {memory_usage}")


if __name__ == '__main__':
    main()
