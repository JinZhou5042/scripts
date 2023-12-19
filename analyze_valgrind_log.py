def categorize_log_by_pid():
    file_path = 'valgrind_output.txt'
    logs_by_pid = {}
    current_pid = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('==') and '==' in line[2:]:
                pid_end_index = line.find('==', 2)
                current_pid = line[2:pid_end_index].strip()
                if current_pid not in logs_by_pid:
                    logs_by_pid[current_pid] = []
                logs_by_pid[current_pid].append(line.strip())
    
    with open('valgrind_formatted_output.txt', 'w') as f:
        for pid, log_entries in logs_by_pid.items():
            f.write(f"PID: {pid}\n")
            for entry in log_entries:
                f.write(f"{entry} \n")


def parse_valgrind_output():

    def convert_kb_to_higher_unit(kb):
        if kb < 1024:
            return f"{kb} KB"
        elif kb < 1024 * 1024:
            return f"{kb / 1024:.2f} MB"
        else:
            return f"{kb / 1024 / 1024:.2f} GB"

    file_path = 'valgrind_formatted_output.txt' 
    total_definitely_lost = 0
    total_indirectly_lost = 0
    num_threads = 0
    leak_summary_active = False

    with open(file_path, 'r') as file:
        for line in file:
            if 'LEAK SUMMARY:' in line:
                leak_summary_active = True
            elif leak_summary_active:
                if 'definitely lost:' in line:
                    lost_memory = int(line.split(':')[1].split('bytes')[0].replace(',', '').strip())
                    total_definitely_lost += lost_memory
                    num_threads += 1
                elif 'indirectly lost:' in line:
                    lost_memory = int(line.split(':')[1].split('bytes')[0].replace(',', '').strip())
                    total_indirectly_lost += lost_memory

                if not any(key in line for key in ['definitely lost', 'indirectly lost', 'possibly lost', 'still reachable']):
                    leak_summary_active = False

    print(f"number of threads = {num_threads}")
    print(f"definitely lost = {convert_kb_to_higher_unit(total_definitely_lost)}") 
    print(f"indirectly lost = {convert_kb_to_higher_unit(total_indirectly_lost)}")


categorize_log_by_pid()
parse_valgrind_output()