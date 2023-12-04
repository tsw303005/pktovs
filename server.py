import subprocess
import re
import os
from time import sleep
from dotenv import load_dotenv

def getNumSoftirqs(irqNum): 
    command = "cat /proc/softirqs | grep -i  NET_RX:"

    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, err = proc.communicate()

    result = re.sub(r'\s+', ' ', output.decode('utf-8'))
    result = re.findall(r'\d+', result)

    if len(irqNum) == 0:
        irqNum = result
    else:
        diff = []
        for index, num in enumerate(irqNum):
            diff.append(int(result[index]) - int(num))
        
        global count
        count += sum(diff)
        irqNum = result

    return irqNum

def cpuUsage():
    command = "sar -u 1 > cpu_utilization.out"
    
    proc = subprocess.Popen(command, shell=True)


def startIperfServer(n):
    commands = [f"{iperf} -s -p {server_port} > /dev/null 2>&1 &" for i in range(n)]
    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]

    for process in processes:
        process.wait()

def iperfVersion():
    command = f"{iperf} -v"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, err = proc.communicate()
    print(f"--------- iperf version --------- \n\n{output.decode('utf-8')}\n")


load_dotenv()
n = int(os.getenv('N')) # n is numer of iperf server
iperf = os.getenv('IPERF_PATH')
server_port = int(os.getenv('SERVER_PORT'))
irqNum = list()
count = 0 # used to collect softirq number

iperfVersion() # get iperf version
print("[Info] start iperf server...")
startIperfServer(n) # run iperf server
cpuUsage() # show cpu usage

while (True):
    irqNum = getNumSoftirqs(irqNum)
    with open("interrupts.out", "w") as f:
        f.write(f"Number of interrupts: {count}")
    sleep(1)
