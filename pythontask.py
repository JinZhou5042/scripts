import ndcctools.taskvine as vine
from tqdm import tqdm
import time
import numpy
import math
import matplotlib.pyplot as plt

def selfadd(num):
    return num + 1

def fn_with_tmp(filename):
    import cloudpickle
    with open(filename) as f:
        data = cloudpickle.load(f)

def main():

    q = vine.Manager(port=9123)
    q.set_name("test_manager")
    print(f"TaskVine manager listening on port {q.port}")

    ta = vine.PythonTask(selfadd, 5)
    # print(f"out file  {ta.output_file}")
    ta.enable_temp_output()
    tid = q.submit(ta)

    while not q.empty():
        t = q.wait(5)
        if t:
            # print(t.output)
            print(f"out file  {ta.output_file}")
            # tb = vine.PythonTask(fn_with_tmp, "ta_output.file")
            # tb.add_input(ta.output_file, "ta_output.file")
            # q.submit(tb)

    # t = q.wait(8)
    # if t:
      #  print(f"t.output = {t.output}")


if __name__ == '__main__':
    main()