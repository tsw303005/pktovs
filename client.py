import subprocess
import os
import json
from dotenv import load_dotenv

# load env
load_dotenv()

n =  int(os.getenv('N')) # n is number of thread
server_addr = os.getenv('SERVER_ADDR')
commands = [f"iperf3 -c {server_addr} -p {5100 + i} -J > {5100 + i}.json" for i in range(n)]

processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]

for process in processes:
    process.wait()

total_transfer_data = 0
bandwidth = 0

for i in range(n):
    with open(f"{5100 + i}.json", "r") as f:
        data = json.load(f)
        total_transfer_data += int(data["end"]["sum_sent"]["bytes"]) * 8
        bandwidth += int(data["end"]["sum_sent"]["bits_per_second"])

print(f"Total transfer data: {total_transfer_data / 1000000000} Gbits")
print(f"Bandwidth: {bandwidth / 1000000000} Gbits/sec")
