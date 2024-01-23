import sys
import matplotlib.pyplot as plt

def read_log_file(log_path):
    with open(log_path, 'r') as file:
        return file.read().splitlines()

def parse_log_line(line):
    try:
        timestamp, process_id, category, obj_id, status, info = line.split(maxsplit=5)
        timestamp = float(timestamp) / 1000000
        return timestamp, process_id, category, obj_id, status, info
    except ValueError:
        return None

def update_task_info(tasks, obj_id, status, info, timestamp):
    """
    Depending on the 'status', updates different attributes of the task such as start time, stop time, worker, and associated function. 
    Also updates and returns the earliest task start time seen so far.
    """
    if obj_id not in tasks:
        tasks[obj_id] = {}
    if status == 'READY':
        function = info.split()[0]
        tasks[obj_id]['function'] = function
    if status == 'RUNNING':
        tasks[obj_id]['start_time'] = timestamp
        tasks[obj_id]['worker'] = info.split()[0]
    if status == 'WAITING_RETRIEVAL':
        tasks[obj_id]['stop_time'] = timestamp


def update_worker_info(workers, obj_id, status, timestamp):
    """
    Handles two types of status updates:
    'CONNECTION' and 'DISCONNECTION', which update the worker's start and stop times, respectively.
    """
    if obj_id not in workers:
        workers[obj_id] = {'tasks': [], 'libraries': []}
    if status == 'CONNECTION':
        workers[obj_id]['start_time'] = timestamp
    if status == 'DISCONNECTION':
        workers[obj_id]['stop_time'] = timestamp

def update_library_info(libraries, obj_id, status, timestamp, info):
    """    
    When a library is marked as 'STARTED', updates the library's start time and the worker associated with it.
    """
    if obj_id not in libraries:
        libraries[obj_id] = {}
    if status == 'STARTED':
        libraries[obj_id]['start_time'] = timestamp
        libraries[obj_id]['worker'] = info

def match_tasks_to_workers(tasks, workers):
    """
    Matches each task with its responsible worker by adding the task to the respective worker's task list in the 'workers' dictionary.
    Only tasks that have a 'stop_time' recorded (indicating completion or termination) are considered for matching.
    """
    for task in tasks:
        worker_id = tasks[task].get('worker')
        if worker_id in workers and 'stop_time' in tasks[task]:
            workers[worker_id]['tasks'].append(tasks[task])

def match_libraries_to_workers(libraries, workers):
    """
    Assigns each library to its managing worker by adding the library details to the corresponding worker's list of libraries in the 'workers' dictionary.
    """
    for library in libraries:
        worker_id = libraries[library].get('worker')
        if worker_id in workers:
            workers[worker_id]['libraries'].append(libraries[library])

def assign_tasks_to_workers(log_path):
    """
    Processes a log file, extracting and organizing task, worker, and library information. 
    Tracks the time the first task was ran, and associates tasks and libraries with workers.
    """
    with open(log_path, 'r') as file:
        log_lines = file.read().splitlines()
    
    task_info = {}
    worker_info = {}
    library_info = {}

    manager_start = manager_end = 0

    for line in log_lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            time, _, category, obj_id, status, info = parsed_line

            if category == 'TASK':
                update_task_info(task_info, obj_id, status, info, time)
            if category == 'WORKER':
                update_worker_info(worker_info, obj_id, status, time)
            if category == 'LIBRARY':
                update_library_info(library_info, obj_id, status, time, info)
            if category == 'MANAGER':
                if status == 'START':
                    manager_start = time
                if status == 'END':
                    manager_end = time

    match_tasks_to_workers(task_info, worker_info)
    match_libraries_to_workers(library_info, worker_info)
                
    return manager_start, manager_end, worker_info


def visualize_tasks_on_workers(worker_info, manager_end, output_file):
    task_data = {
        'general': {'y_positions': [], 'widths': [], 'start_positions': []},
        'library': {'y_positions': [], 'widths': [], 'start_positions': []}
    }

    first_task_start = float('inf')
    for worker in worker_info:
        for task in worker_info[worker]['tasks']:
            task_start = task['start_time']
            first_task_start = min(task_start, first_task_start)

    task_counter = 0
    total_task_count = 0
    total_assigned_tasks = 0

    def add_task_to_slots(slots, task):
        for slot_number, slot_tasks in slots.items():
            if task[0] > slot_tasks[-1][1]:
                slot_tasks.append(task)
                return True
        return False

    for worker, info in worker_info.items():
        print(f"=== {worker}")
        slots = {}
        tasks = sorted(
            [[task['start_time'], task['stop_time'], task['function']] for task in info['tasks']], 
            key=lambda x: x[0]
        )

        print('number of tasks:', len(tasks))
        total_task_count += len(tasks)

        for task in tasks:
            if not slots:
                slots[1] = [task]
            else:
                if not add_task_to_slots(slots, task):
                    slots[len(slots) + 1] = [task]

        print('number of slots:', len(slots))

        for slot_tasks in slots.values():
            total_assigned_tasks += len(slot_tasks)
            task_counter += 1
            for task in slot_tasks:
                task_type = 'random' if 'random' in task[2] else 'general'
                task_data[task_type]['y_positions'].append(task_counter)
                task_data[task_type]['widths'].append(task[1] - task[0])
                task_data[task_type]['start_positions'].append(task[0] - first_task_start)

        for library in info['libraries']:
            task_counter += 1
            task_data['library']['y_positions'].append(task_counter)
            task_data['library']['widths'].append(manager_end - library['start_time'])
            task_data['library']['start_positions'].append(library['start_time'] - first_task_start)

    print('assigned:', total_assigned_tasks)
    print('total tasks:', total_task_count)

    if task_data['general']['y_positions']:
        plt.barh(task_data['general']['y_positions'], task_data['general']['widths'], left=task_data['general']['start_positions'], label='General Tasks', color='orange')

    if task_data['library']['y_positions']:
        plt.barh(task_data['library']['y_positions'], task_data['library']['widths'], left=task_data['library']['start_positions'], label='Library Tasks', color='green')

    plt.tick_params(axis='y', labelleft=False)
    plt.xlabel('Time (s)')
    plt.legend()
    plt.savefig(output_file)
    plt.show()


if __name__ == '__main__':
    log_file_path = sys.argv[1]
    out_png_path = sys.argv[2]

    manager_start, manager_end, worker_info = assign_tasks_to_workers(log_file_path)
    visualize_tasks_on_workers(worker_info, manager_end, out_png_path)
