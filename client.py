import subprocess
import os
import json
from dotenv import load_dotenv

def iperfVersion():
    command = f"{iperf} -v"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, err = proc.communicate()
    print(f"--------- iperf version --------- \n\n{output.decode('utf-8')}\n")

# load env
load_dotenv()
n =  int(os.getenv('N')) # n is number of thread
server_addr = os.getenv('SERVER_ADDR')
server_port = int(os.getenv('SERVER_PORT'))
iperf = os.getenv('IPERF_PATH') # iperf path

iperfVersion() # get iperf version
print(f"[Info] start iperf client, number of threads: {n}...")

# luanch iperf process
commands = [f"{iperf} -c {server_addr} -P {n} -p {server_port} -J > result.json" for i in range(n)]
processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]
for process in processes:
    process.wait()

total_transfer_data = 0
bandwidth = 0

with open(f"result.json", "r") as f:
    data = json.load(f)
    total_transfer_data += int(data["end"]["sum_sent"]["bytes"]) * 8
    bandwidth += int(data["end"]["sum_sent"]["bits_per_second"])

print(f"Total transfer data: {total_transfer_data / 1000000000} Gbits")
print(f"Bandwidth: {bandwidth / 1000000000} Gbits/sec")
