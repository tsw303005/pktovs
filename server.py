import subprocess
import re
from time import sleep

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
    commands = [f"iperf3 -s -p {5100 + i} > /dev/null 2>&1 &" for i in range(n)]
    processes = [subprocess.Popen(cmd, shell=True) for cmd in commands]

    for process in processes:
        process.wait()


n = 7 # n is numer of iperf server
irqNum = list()
count = 0
startIperfServer(n)
cpuUsage()
while (True):
    irqNum = getNumSoftirqs(irqNum)
    with open("interrupts.out", "w") as f:
        f.write(f"Number of interrupts: {count}")
    sleep(1)
