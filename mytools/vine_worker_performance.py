#! /usr/bin/env python

# Copyright (C) 2023- The University of Notre Dame
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

# Plot the time spent matching tasks to workers through the information in the performance log

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def read_fields(f, lines_patience = 10):
    for line in f:
        if line[0] != '#':
            lines_patience = lines_patience - 1
        else:
            return line.strip('#\n\r\t ').split()
        if lines_patience < 1:
            break
    sys.stderr.write("Could not find fields. This is probably not a performance log...\n")
    sys.exit(1)


if __name__ == "__main__":
    """ This script processes a performance file and generates corresponding output figures
     showing the busy and idle times of workers while running this application. The output figures
     will be saved in the same folder as the input performance log file """

    log_performance = sys.argv[1]
    f = open(log_performance)
    fields = read_fields(f)
    f.seek(0)
    
    timestamp_offset = fields.index("timestamp")
    workers_connected_offset = fields.index("workers_connected")
    workers_idle_offset = fields.index("workers_idle")
    workers_busy_offset = fields.index("workers_busy")
    tasks_done_offset = fields.index("tasks_done")

    timestamps = []
    workers_connected = []
    workers_idle = []
    workers_busy = []
    tasks_done = []    
    last_task_done_item = -1  

    for line in f:
        if line[0] == "#":
            continue
        items = line.strip("\n\r\t ").split()
        
        timestamp_item = int(items[timestamp_offset])
        workers_connected_item = int(items[workers_connected_offset])
        workers_idle_item = int(items[workers_idle_offset])
        workers_busy_item = int(items[workers_busy_offset])
        task_done_item = int(items[tasks_done_offset])

        if len(tasks_done) > 1 and task_done_item == tasks_done[-1]:
            continue
        
        if len(tasks_done) > 1 and task_done_item - tasks_done[-1] > 1:
            for i_ in range(tasks_done[-1], task_done_item, 1):
                timestamps.append(timestamp_item)
                workers_connected.append(workers_connected_item)
                workers_idle.append(workers_idle_item) 
                workers_busy.append(workers_busy_item)
                tasks_done.append(i_)
        
        timestamps.append(timestamp_item)
        workers_connected.append(workers_connected_item)
        workers_idle.append(workers_idle_item) 
        workers_busy.append(workers_busy_item)
        tasks_done.append(task_done_item)
                 
    num_workers = max(workers_connected)
    num_tasks = tasks_done[-1]

    base_timestamp = timestamps[0]
    for id, timestamp in enumerate(timestamps):
        timestamps[id] -= base_timestamp
        timestamps[id] /= 1e6

    plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[0, 1])

    busy_color = "#ae232d"
    idle_color = "#979797"

    ax1.plot(timestamps, workers_busy, color=busy_color, label='busy')
    ax1.plot(timestamps, workers_idle, color=idle_color, label='idle')
    ax1.set_xlabel("Total Time (s)")
    ax1.set_ylabel("Number of Workers")
    ax1.legend()

    ax2.bar(tasks_done, workers_busy, color=busy_color, label='busy', width=1)
    ax2.bar(tasks_done, workers_idle, color=idle_color, bottom=workers_busy, label='idle', width=1)
    ax2.set_xlabel("Tasks Done")
    ax2.set_ylabel("Number of Workers")
    ax2.legend()

    plt.tight_layout()
    plt.show()

    save_png = os.path.join(os.path.dirname(log_performance), "worker_performance")
    plt.savefig(save_png)