import pandas as pd
import subprocess
import re

def get_hostnames():
    proc = subprocess.Popen(['condor_status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 0 and stdout:
        data = stdout.decode('utf-8')
        addresses = set(re.findall(r'@([\w\.\-]+)', data))
        return list(addresses)

def clean_value(value):
    for i in range(3):
        value = value.strip().strip('"').strip("'").strip('$')
    return value
    

def parse_right(result, key, line):
    if line.startswith(key):
        right_value = clean_value(line.split("=")[1])
        if right_value == '':
            result[key] = None
        if key == 'cpu_model':
            if '@' in line:
                result['cpu_frequency'] = clean_value(right_value.split('@')[1])
                result['cpu_model'] = clean_value(right_value.split('@')[0])
            else:
                result['cpu_frequency'] = right_value
                result['cpu_frequency'] = 'unknown'
        elif key == 'CondorVersion':
            match = re.search(r"CondorVersion:\s*([^\s]+).*?BuildID:\s*([^\s]+)", right_value)
            if match:
                result['Condor_Version'], result['Condor_Build_ID'] = match.groups()
            else:
                result['Condor_Version'], result['Condor_Build_ID'] = 'Unkown', 'Unkown'
        else:
            result[key] = right_value

def get_condor_status(hostname):
    command = f"condor_status -long {hostname}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Command failed with error: {stderr.decode()}")

    output_lines = stdout.decode().split("\n")
    result = {}
    result["hostname"] = hostname
    key = None
    cnt_AcceptedWhileDraining = 0
    for line in output_lines:
        if "AcceptedWhileDraining" in line:
            cnt_AcceptedWhileDraining += 1
            if cnt_AcceptedWhileDraining == 2:
                break;
        parse_right(result, "cpu_model", line) 
        parse_right(result, "eth_link_speed", line) 
        parse_right(result, "DetectedCpus", line) 
        parse_right(result, "DetectedMemory", line) 
        parse_right(result, "Disk", line) 
        parse_right(result, "KFlops", line) 
        parse_right(result, "Mips", line) 
        parse_right(result, "JavaMFlops", line) 
        parse_right(result, "JobPreemptions", line)
        parse_right(result, "JobRankPreemptions", line)
        parse_right(result, "has_scratch365", line) 
        parse_right(result, "glibc_version", line) 
        parse_right(result, "OpSysLongName", line) 
        parse_right(result, "CpuCacheSize", line) 
        parse_right(result, "CondorVersion", line) 
        parse_right(result, "has_afs", line) 
        parse_right(result, "has_avx", line) 
        parse_right(result, "has_avx2", line) 
        parse_right(result, "has_singularity", line) 
        parse_right(result, "has_sse4_1", line) 
        parse_right(result, "has_sse4_2", line) 
        parse_right(result, "has_ssse3", line) 
        parse_right(result, "has_vast", line) 
        parse_right(result, "HasFileTransfer", line) 
        parse_right(result, "HasJICLocalConfig", line) 
        parse_right(result, "HasJobDeferral", line) 
        parse_right(result, "HasMPI", line) 
        parse_right(result, "HasTDP", line) 
        parse_right(result, "HasVM", line) 
        parse_right(result, "HasTransferInputRemaps", line) 
        
    return result

all_hostnames = get_hostnames()
all_worker_status = {}
for hostname in all_hostnames:
    print(f"parsing {hostname}")
    all_worker_status[hostname] = get_condor_status(hostname) 
all_worker_status = pd.DataFrame.from_dict(all_worker_status, "index")

all_worker_status.to_csv('all_worker_configs.csv', index=False)

