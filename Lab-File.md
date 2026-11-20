# OPERATING SYSTEMS

## Practical File

CSC301: Operating Systems

B.Sc. (CS) — Third Year

*Programming Language: Python*

*Submitted by :* Arnav Gairola
*Roll no :* 2472020

## List of Programs

| S.No. | Title of Program |
|---|---|
| 1 | Introduction to Linux System Calls, Process Creation using fork(), exec() and wait() |
| 2 | Thread Creation and Management using POSIX Threads (pthreads) |
| 3 | CPU Scheduling Algorithms — FCFS, SJF, Priority and Round Robin |
| 4 | Process Synchronization — Producer-Consumer Problem using Semaphores |
| 5 | Process Synchronization — Readers-Writers Problem using Semaphores |
| 6 | Dining Philosophers Problem using Semaphores |
| 7 | Deadlock Avoidance using Banker's Algorithm |
| 8 | Contiguous Memory Allocation — First Fit, Best Fit and Worst Fit |
| 9 | Page Replacement Algorithms — FIFO, LRU and Optimal |
| 10 | Disk Scheduling Algorithms — FCFS, SSTF, SCAN and C-SCAN |
| 11 | File Allocation Methods — Contiguous, Linked and Indexed Allocation |

## Program 1

**Introduction to Linux System Calls, Process Creation using fork(), exec() and wait()**

| Aim | To study basic Linux/UNIX system calls related to process management and to write Python programs using fork(), exec() family and wait() system calls to create and manage child processes. |
|---|---|

### Theory

A process is a program in execution. Every process in UNIX/Linux is identified by a unique Process ID (PID). The operating system provides system calls to create, control and terminate processes.

fork() creates a new process (child) which is an almost exact copy of the calling (parent) process. It returns 0 in the child, the child's PID in the parent, and -1 on failure.

The exec() family of functions (execl, execv, execlp, execvp, execve) replaces the current process image with a new program. The PID does not change; only the code, data and stack are replaced.

wait()/waitpid() suspends execution of the calling process until one of its children terminates, and allows the parent to collect the child's exit status, preventing zombie processes.

getpid() returns the process ID of the calling process; getppid() returns the parent's process ID.

### Program (Python)

```python
import os
import sys

print(f"Parent process: PID = {os.getpid()}", flush=True)

try:
    pid = os.fork()
except OSError as e:
    # fork failed
    print(f"fork failed: {e.strerror}")
    sys.exit(1)

if pid == 0:
    # Child process
    print(f"Child process: PID = {os.getpid()}, Parent PID = {os.getppid()}")
    print("Child is about to exec 'ls -l'", flush=True)
    try:
        os.execlp("ls", "ls", "-l")
    except OSError as e:
        # execlp only returns on error
        print(f"exec failed: {e.strerror}")
        os._exit(1)
else:
    # Parent process
    print(f"Parent waiting for child (PID = {pid}) to finish...", flush=True)
    _, status = os.wait()
    if os.WIFEXITED(status):
        print(f"Child exited with status {os.WEXITSTATUS(status)}")
    print("Parent process resumes and exits.")
```

### Execution

```bash
python3 fork_exec.py
```

### Sample Output

```text
Parent process: PID = 4521
Parent waiting for child (PID = 4522) to finish...
Child process: PID = 4522, Parent PID = 4521
Child is about to exec 'ls -l'
total 4
-rw-r--r-- 1 user user 817 Sep  3 09:09 fork_exec.py
Child exited with status 0
Parent process resumes and exits.
```

### Viva-Voce Questions

1. What is the difference between a process and a program?
2. What value does fork() return in the parent and in the child?
3. Why does exec() not change the PID of the process?
4. What is a zombie process and how does wait() prevent it?
5. What is an orphan process?
6. Differentiate between execl(), execv(), execlp() and execvp().

## Program 2

**Thread Creation and Management using POSIX Threads (pthreads)**

| Aim | To understand the concept of threads and write a multithreaded Python program using the threading module to create, synchronize and join threads. |
|---|---|

### Theory

A thread is the smallest unit of CPU execution within a process. Multiple threads within the same process share the same address space (code, data, heap and open files) but have their own stack, program counter and registers.

POSIX threads (pthreads) is a standard threading API for UNIX-like systems. Key functions include pthread_create() to create a new thread, pthread_join() to wait for a thread to finish, and pthread_exit() to terminate a thread.

Multithreading improves responsiveness and allows parallel execution of independent tasks on multicore processors, but requires synchronization when threads share data.

### Program (Python)

```python
import sys
import threading

NUM_THREADS = 4


def safe_print(msg):
    # print() writes the text and the newline separately, so lines from
    # different threads can get mixed up; a single write() keeps each line intact
    sys.stdout.write(msg + "\n")


class PartialSum:
    """argument and result passed to each thread"""
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sum = 0


def sum_array(p):
    p.sum = 0
    for i in range(p.start, p.end):
        p.sum += i
    safe_print(f"Thread {threading.get_ident() % 100000}: "
               f"sum[{p.start}..{p.end}) = {p.sum}")


def main():
    n = 1000000
    chunk = n // NUM_THREADS
    total = 0
    threads = []
    data = []

    for i in range(NUM_THREADS):
        start = i * chunk
        end = n if i == NUM_THREADS - 1 else (i + 1) * chunk
        data.append(PartialSum(start, end))
        t = threading.Thread(target=sum_array, args=(data[i],))
        threads.append(t)
        t.start()

    for i in range(NUM_THREADS):
        threads[i].join()
        total += data[i].sum

    print(f"Total sum (0 to {n - 1}) computed using {NUM_THREADS} threads = {total}")


main()
```

### Execution

```bash
python3 thread_sum.py
```

### Sample Output

```text
Thread 6432: sum[250000..500000) = 93749875000
Thread 99136: sum[0..250000) = 31249875000
Thread 13728: sum[500000..750000) = 156249875000
Thread 21024: sum[750000..1000000) = 218749875000
Total sum (0 to 999999) computed using 4 threads = 499999500000
```

### Viva-Voce Questions

1. What is the difference between a process and a thread?
2. What are the advantages of multithreading?
3. What is the purpose of pthread_join()?
4. What happens if the main thread exits before other threads finish?
5. What is thread-safety and why is it needed?
6. Name the multithreading models (many-to-one, one-to-one, many-to-many).

## Program 3

**CPU Scheduling Algorithms — FCFS, SJF, Priority and Round Robin**

| Aim | To implement and compare non-preemptive First Come First Served (FCFS), Shortest Job First (SJF), Priority scheduling, and preemptive Round Robin CPU scheduling algorithms, and compute average waiting time and turnaround time. |
|---|---|

### Theory

CPU scheduling decides which of the ready processes is allocated the CPU. FCFS executes processes strictly in order of arrival — simple but can cause the convoy effect.

SJF (non-preemptive) selects the process with the smallest burst time among the available processes; it minimizes average waiting time but can cause starvation of longer jobs.

Priority scheduling allocates the CPU to the process with the highest priority (here, lower number = higher priority); it can also cause starvation, solved using aging.

Round Robin allocates the CPU to each ready process for a fixed time quantum in cyclic order — it is preemptive and provides fair, responsive scheduling suitable for time-sharing systems.

Waiting Time = Turnaround Time − Burst Time,  Turnaround Time = Completion Time − Arrival Time.

### Program (Python)

```python
from collections import deque


class Process:
    def __init__(self, pid, at, bt, pr):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.pr = pr
        self.ct = self.tat = self.wt = 0
        self.rem = 0


def print_result(p):
    n = len(p)
    total_wt = total_tat = 0
    print("\nPID\tAT\tBT\tCT\tTAT\tWT")
    for x in p:
        print(f"{x.pid}\t{x.at}\t{x.bt}\t{x.ct}\t{x.tat}\t{x.wt}")
        total_wt += x.wt
        total_tat += x.tat
    print(f"Average Waiting Time    = {total_wt / n:.2f}")
    print(f"Average Turnaround Time = {total_tat / n:.2f}")


def finish(x, time):
    x.ct = time
    x.tat = x.ct - x.at
    x.wt = x.tat - x.bt


def fcfs(p):
    time = 0
    for x in p:
        if time < x.at:
            time = x.at
        time += x.bt
        finish(x, time)
    print_result(p)


def sjf(p):
    n = len(p)
    completed, time = 0, 0
    done = [False] * n
    while completed < n:
        idx, min_bt = -1, 10**9
        for i in range(n):
            if not done[i] and p[i].at <= time and p[i].bt < min_bt:
                min_bt = p[i].bt
                idx = i
        if idx == -1:
            time += 1
            continue
        time += p[idx].bt
        finish(p[idx], time)
        done[idx] = True
        completed += 1
    print_result(p)


def priority_scheduling(p):
    n = len(p)
    completed, time = 0, 0
    done = [False] * n
    while completed < n:
        idx, best = -1, 10**9
        for i in range(n):
            if not done[i] and p[i].at <= time and p[i].pr < best:
                best = p[i].pr
                idx = i
        if idx == -1:
            time += 1
            continue
        time += p[idx].bt
        finish(p[idx], time)
        done[idx] = True
        completed += 1
    print_result(p)


def round_robin(p, quantum):
    n = len(p)
    time, completed = 0, 0
    for x in p:
        x.rem = x.bt

    queue = deque()
    in_queue = [False] * n

    # start with process(es) arriving at time 0, in PID order
    for i in range(n):
        if p[i].at <= time:
            queue.append(i)
            in_queue[i] = True

    while completed < n:
        if not queue:
            time += 1
            for i in range(n):
                if not in_queue[i] and p[i].rem > 0 and p[i].at <= time:
                    queue.append(i)
                    in_queue[i] = True
            continue
        idx = queue.popleft()
        slice_ = min(p[idx].rem, quantum)
        time += slice_
        p[idx].rem -= slice_

        for i in range(n):
            if not in_queue[i] and p[i].rem > 0 and p[i].at <= time and i != idx:
                queue.append(i)
                in_queue[i] = True

        if p[idx].rem > 0:
            queue.append(idx)
        else:
            finish(p[idx], time)
            completed += 1
            in_queue[idx] = False
    print_result(p)


def main():
    n = int(input("Enter number of processes: "))
    p = []
    for i in range(n):
        at, bt, pr = map(int, input(
            f"Process {i + 1} - Arrival Time, Burst Time, Priority: ").split())
        p.append(Process(i + 1, at, bt, pr))

    print("\nMenu:\n1. FCFS\n2. SJF (Non-preemptive)")
    print("3. Priority (Non-preemptive)\n4. Round Robin")
    choice = int(input("Enter choice: "))

    if choice == 1:
        fcfs(p)
    elif choice == 2:
        sjf(p)
    elif choice == 3:
        priority_scheduling(p)
    elif choice == 4:
        quantum = int(input("Enter time quantum: "))
        round_robin(p, quantum)
    else:
        print("Invalid choice")


main()
```

### Execution

```bash
python3 scheduling.py
```

### Sample Output

```text
Enter number of processes: 4
Process 1 - Arrival Time, Burst Time, Priority: 0 5 2
Process 2 - Arrival Time, Burst Time, Priority: 1 3 1
Process 3 - Arrival Time, Burst Time, Priority: 2 8 3
Process 4 - Arrival Time, Burst Time, Priority: 3 6 4
 
Menu:
1. FCFS
2. SJF (Non-preemptive)
3. Priority (Non-preemptive)
4. Round Robin
Enter choice: 4
Enter time quantum: 4
 
PID  AT  BT  CT  TAT  WT
1    0   5   16  16   11
2    1   3   7   6    3
3    2   8   20  18   10
4    3   6   22  19   13
Average Waiting Time    = 9.25
Average Turnaround Time = 14.75
```

### Viva-Voce Questions

1. What is the convoy effect in FCFS scheduling?
2. Why is SJF called optimal in terms of average waiting time?
3. How does the choice of time quantum affect Round Robin performance?
4. What is starvation, and which of these algorithms suffer from it?
5. Differentiate preemptive and non-preemptive scheduling.
6. What is the difference between waiting time and turnaround time?

## Program 4

**Process Synchronization — Producer-Consumer Problem using Semaphores**

| Aim | To implement the classical Producer-Consumer (Bounded Buffer) problem using semaphores and threads to achieve mutual exclusion and synchronization. |
|---|---|

### Theory

The Producer-Consumer problem involves two types of processes/threads sharing a fixed-size buffer: producers add items, and consumers remove them.

Synchronization must ensure the producer does not add to a full buffer and the consumer does not remove from an empty buffer, and that access to the shared buffer is mutually exclusive.

This is solved using three semaphores: 'empty' (counts empty slots, initialized to buffer size), 'full' (counts filled slots, initialized to 0), and 'mutex' (binary semaphore for mutual exclusion, initialized to 1).

### Program (Python)

```python
import sys
import threading
import time

BUFFER_SIZE = 5
ITEMS = 10

buffer = [0] * BUFFER_SIZE
in_idx = 0
out_idx = 0

empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)


def safe_print(msg):
    # print() writes the text and the newline separately, so lines from
    # different threads can get mixed up; a single write() keeps each line intact
    sys.stdout.write(msg + "\n")


def producer():
    global in_idx
    for i in range(1, ITEMS + 1):
        empty.acquire()
        mutex.acquire()

        buffer[in_idx] = i
        safe_print(f"Producer produced item {i} at slot {in_idx}")
        in_idx = (in_idx + 1) % BUFFER_SIZE

        mutex.release()
        full.release()
        time.sleep(0.1)


def consumer():
    global out_idx
    for _ in range(1, ITEMS + 1):
        full.acquire()
        mutex.acquire()

        item = buffer[out_idx]
        safe_print(f"\t\tConsumer consumed item {item} from slot {out_idx}")
        out_idx = (out_idx + 1) % BUFFER_SIZE

        mutex.release()
        empty.release()
        time.sleep(0.15)


prod = threading.Thread(target=producer)
cons = threading.Thread(target=consumer)

prod.start()
cons.start()

prod.join()
cons.join()

print("All items produced and consumed.")
```

### Execution

```bash
python3 producer_consumer.py
```

### Sample Output

```text
Producer produced item 1 at slot 0
                Consumer consumed item 1 from slot 0
Producer produced item 2 at slot 1
                Consumer consumed item 2 from slot 1
Producer produced item 3 at slot 2
                Consumer consumed item 3 from slot 2
...
All items produced and consumed.
```

### Viva-Voce Questions

1. Why are three semaphores needed instead of one?
2. What is the difference between a binary semaphore and a counting semaphore?
3. What happens if sem_wait(&mutex) is called before sem_wait(&empty) inside the producer?
4. What is a race condition?
5. Define the critical section problem and its three requirements.
6. How do semaphores differ from mutex locks and monitors?

## Program 5

**Process Synchronization — Readers-Writers Problem using Semaphores**

| Aim | To implement the first Readers-Writers problem using semaphores, allowing multiple readers to read a shared resource concurrently while ensuring writers get exclusive access. |
|---|---|

### Theory

The Readers-Writers problem models access to a shared resource (e.g., a file or database) by multiple reader and writer threads.

Rules: multiple readers may read simultaneously; a writer requires exclusive access (no other reader or writer may access the resource while it writes).

This classic (first) solution uses a semaphore 'wrt' for exclusive writer access, a semaphore 'mutex' to protect the shared counter 'read_count', which tracks the number of active readers. The resource is locked by the first reader and unlocked by the last reader; this variant may starve writers.

### Program (Python)

```python
import sys
import threading
import time

mutex = threading.Semaphore(1)
wrt = threading.Semaphore(1)
read_count = 0
shared_data = 0


def safe_print(msg):
    # print() writes the text and the newline separately, so lines from
    # different threads can get mixed up; a single write() keeps each line intact
    sys.stdout.write(msg + "\n")


def reader(rid):
    global read_count

    mutex.acquire()
    read_count += 1
    if read_count == 1:
        wrt.acquire()            # first reader locks the resource
    mutex.release()

    safe_print(f"Reader {rid}: read shared_data = {shared_data}")
    time.sleep(0.2)

    mutex.acquire()
    read_count -= 1
    if read_count == 0:
        wrt.release()            # last reader unlocks the resource
    mutex.release()


def writer(wid):
    global shared_data

    wrt.acquire()
    shared_data += 1
    safe_print(f"Writer {wid}: wrote shared_data = {shared_data}")
    time.sleep(0.3)
    wrt.release()


r = [None] * 5
w = [None] * 2

w[0] = threading.Thread(target=writer, args=(1,))
w[0].start()
for i in range(5):
    r[i] = threading.Thread(target=reader, args=(i + 1,))
    r[i].start()
w[1] = threading.Thread(target=writer, args=(2,))
w[1].start()

for i in range(5):
    r[i].join()
w[0].join()
w[1].join()
```

### Execution

```bash
python3 readers_writers.py
```

### Sample Output

```text
Writer 1: wrote shared_data = 1
Reader 1: read shared_data = 1
Reader 2: read shared_data = 1
Reader 3: read shared_data = 1
Reader 4: read shared_data = 1
Reader 5: read shared_data = 1
Writer 2: wrote shared_data = 2
```

### Viva-Voce Questions

1. What is the difference between the first and second Readers-Writers problems?
2. Why can multiple readers access the resource simultaneously but not writers?
3. How does this solution risk starving writers?
4. What role does the read_count variable play?
5. How would you modify the code to give writers priority?

## Program 6

**Dining Philosophers Problem using Semaphores**

| Aim | To implement the Dining Philosophers problem using semaphores in a way that avoids deadlock, illustrating concurrency control among multiple processes sharing limited resources (forks). |
|---|---|

### Theory

Five philosophers sit around a table with five forks (one between each pair). Each philosopher alternately thinks and eats; to eat, a philosopher needs both the left and right fork.

If every philosopher picks up the left fork first, all may simultaneously hold one fork and wait forever for the right fork — a circular wait, causing deadlock.

Deadlock is avoided here by allowing at most (N-1) philosophers to try to pick up forks at the same time, using a counting semaphore, which breaks the circular-wait condition.

### Program (Python)

```python
import sys
import threading
import time

N = 5

forks = [threading.Semaphore(1) for _ in range(N)]
room = threading.Semaphore(N - 1)   # allows at most N-1 philosophers to sit and pick up forks


def safe_print(msg):
    # print() writes the text and the newline separately, so lines from
    # different threads can get mixed up; a single write() keeps each line intact
    sys.stdout.write(msg + "\n")


def philosopher(pid):
    left = pid
    right = (pid + 1) % N

    for _ in range(2):
        safe_print(f"Philosopher {pid} is thinking")
        time.sleep(0.1)

        room.acquire()             # enter the "room" - avoids deadlock
        forks[left].acquire()      # pick up left fork
        forks[right].acquire()     # pick up right fork

        safe_print(f"Philosopher {pid} is eating (fork {left} and fork {right})")
        time.sleep(0.15)

        forks[right].release()
        forks[left].release()
        room.release()

        safe_print(f"Philosopher {pid} finished eating and put down forks")


philo = []
for i in range(N):
    t = threading.Thread(target=philosopher, args=(i,))
    philo.append(t)
    t.start()

for t in philo:
    t.join()
```

### Execution

```bash
python3 dining_philosophers.py
```

### Sample Output

```text
Philosopher 0 is thinking
Philosopher 1 is thinking
Philosopher 2 is thinking
Philosopher 3 is thinking
Philosopher 4 is thinking
Philosopher 2 is eating (fork 2 and fork 3)
Philosopher 0 is eating (fork 0 and fork 1)
Philosopher 2 finished eating and put down forks
Philosopher 0 finished eating and put down forks
Philosopher 4 is eating (fork 4 and fork 0)
Philosopher 1 is eating (fork 1 and fork 2)
Philosopher 0 is thinking
...
```

### Viva-Voce Questions

1. What are the four necessary conditions for deadlock?
2. Which condition does the 'room' semaphore break in this solution?
3. What other strategies can avoid deadlock in this problem (e.g., resource ordering, asymmetric approach)?
4. What is the difference between deadlock avoidance and deadlock prevention?
5. Can starvation still occur in this solution?

## Program 7

**Deadlock Avoidance using Banker's Algorithm**

| Aim | To implement the Banker's Algorithm to check whether a system is in a safe state, and to simulate resource allocation requests, thereby avoiding deadlock. |
|---|---|

### Theory

The Banker's Algorithm is a deadlock-avoidance algorithm that tests whether granting a resource request leaves the system in a safe state before actually allocating resources.

It uses four data structures: Available (resources currently free), Max (maximum demand of each process), Allocation (resources currently allocated to each process), and Need = Max − Allocation.

The Safety Algorithm finds a sequence in which all processes can finish without deadlock by repeatedly finding a process whose Need can be satisfied by Available, then simulating its completion (adding its allocation back to Available).

The Resource-Request Algorithm grants a request only if the resulting state (obtained by tentatively allocating) is still safe; otherwise the requesting process must wait.

### Program (Python)

```python
P = 5   # number of processes
R = 3   # number of resource types

available = [0] * R
maximum = [[0] * R for _ in range(P)]
allocation = [[0] * R for _ in range(P)]
need = [[0] * R for _ in range(P)]


def calculate_need():
    for i in range(P):
        for j in range(R):
            need[i][j] = maximum[i][j] - allocation[i][j]


def is_safe(safe_seq):
    work = available[:]
    finish = [False] * P
    safe_seq.clear()

    count = 0
    while count < P:
        found = False
        for i in range(P):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(R)):
                    for k in range(R):
                        work[k] += allocation[i][k]
                    safe_seq.append(i)
                    count += 1
                    finish[i] = True
                    found = True
        if not found:
            return False    # no process could proceed: unsafe
    return True


def request_resources(pid, request):
    for j in range(R):
        if request[j] > need[pid][j]:
            print("Error: process has exceeded its maximum claim.")
            return False
        if request[j] > available[j]:
            print("Request denied: not enough resources available.")
            return False

    # tentatively allocate
    for j in range(R):
        available[j] -= request[j]
        allocation[pid][j] += request[j]
        need[pid][j] -= request[j]

    safe_seq = []
    if is_safe(safe_seq):
        print("Request can be granted safely.")
        return True
    else:
        # rollback
        for j in range(R):
            available[j] += request[j]
            allocation[pid][j] -= request[j]
            need[pid][j] += request[j]
        print("Request denied: would lead to an unsafe state.")
        return False


def main():
    global available, maximum, allocation

    available = list(map(int, input(
        f"Enter available resources of each type ({R} types): ").split()))

    print(f"Enter Maximum matrix ({P} processes x {R} resources):")
    maximum = [list(map(int, input().split())) for _ in range(P)]

    print("Enter Allocation matrix:")
    allocation = [list(map(int, input().split())) for _ in range(P)]

    calculate_need()

    safe_seq = []
    if is_safe(safe_seq):
        print("System is in a SAFE state.")
        print("Safe sequence:", " ".join(f"P{i}" for i in safe_seq))
    else:
        print("System is in an UNSAFE state.")

    pid = int(input("\nEnter process number requesting resources: "))
    request = list(map(int, input(f"Enter request vector ({R} values): ").split()))

    request_resources(pid, request)


main()
```

### Execution

```bash
python3 bankers.py
```

### Sample Output

```text
Enter available resources of each type (3 types): 3 3 2
Enter Maximum matrix (5 processes x 3 resources):
7 5 3
3 2 2
9 0 2
2 2 2
4 3 3
Enter Allocation matrix:
0 1 0
2 0 0
3 0 2
2 1 1
0 0 2
 
System is in a SAFE state.
Safe sequence: P1 P3 P4 P0 P2
 
Enter process number requesting resources: 1
Enter request vector (3 values): 1 0 2
Request can be granted safely.
```

### Viva-Voce Questions

1. State the four necessary conditions for deadlock to occur.
2. What is the difference between deadlock avoidance and deadlock detection?
3. Why is the Banker's Algorithm named so?
4. What is the time complexity of the safety algorithm?
5. What information must be known in advance for the Banker's Algorithm to work?
6. What is a 'safe state' versus an 'unsafe state'?

## Program 8

**Contiguous Memory Allocation — First Fit, Best Fit and Worst Fit**

| Aim | To implement First Fit, Best Fit and Worst Fit memory allocation strategies for contiguous memory partitioning and compare their block allocation and fragmentation. |
|---|---|

### Theory

In contiguous memory allocation, each process is allocated a single contiguous block of memory from a list of free memory blocks (holes).

First Fit allocates the first hole that is big enough — fast, but can leave many small unusable fragments at the start of memory.

Best Fit allocates the smallest hole that is big enough — minimizes leftover space per allocation but leaves many tiny unusable fragments over time and is slower (searches the entire list).

Worst Fit allocates the largest available hole — leaves the largest possible leftover fragment, which may remain usable for future requests.

### Program (Python)

```python
def print_table(title, psize, allocation):
    print(f"\n--- {title} ---")
    print("Process No.\tProcess Size\tBlock No.")
    for i in range(len(psize)):
        print(f"P{i + 1}\t\t{psize[i]}\t\t", end="")
        if allocation[i] != -1:
            print(f"B{allocation[i] + 1}")
        else:
            print("Not Allocated")


def first_fit(bsize, psize):
    block = bsize[:]
    allocation = [-1] * len(psize)

    for i in range(len(psize)):
        for j in range(len(block)):
            if block[j] >= psize[i]:
                allocation[i] = j
                block[j] -= psize[i]
                break
    print_table("First Fit", psize, allocation)


def best_fit(bsize, psize):
    block = bsize[:]
    allocation = [-1] * len(psize)

    for i in range(len(psize)):
        best_idx = -1
        for j in range(len(block)):
            if block[j] >= psize[i]:
                if best_idx == -1 or block[j] < block[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            block[best_idx] -= psize[i]
    print_table("Best Fit", psize, allocation)


def worst_fit(bsize, psize):
    block = bsize[:]
    allocation = [-1] * len(psize)

    for i in range(len(psize)):
        worst_idx = -1
        for j in range(len(block)):
            if block[j] >= psize[i]:
                if worst_idx == -1 or block[j] > block[worst_idx]:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            block[worst_idx] -= psize[i]
    print_table("Worst Fit", psize, allocation)


def main():
    int(input("Enter number of memory blocks: "))
    bsize = list(map(int, input("Enter sizes of blocks: ").split()))

    int(input("Enter number of processes: "))
    psize = list(map(int, input("Enter sizes of processes: ").split()))

    first_fit(bsize, psize)
    best_fit(bsize, psize)
    worst_fit(bsize, psize)


main()
```

### Execution

```bash
python3 memory_allocation.py
```

### Sample Output

```text
Enter number of memory blocks: 5
Enter sizes of blocks: 100 500 200 300 600
Enter number of processes: 4
Enter sizes of processes: 212 417 112 426
 
--- First Fit ---
Process No.  Process Size  Block No.
P1           212           B2
P2           417           B5
P3           112           B2
P4           426           Not Allocated
 
--- Best Fit ---
Process No.  Process Size  Block No.
P1           212           B4
P2           417           B2
P3           112           B3
P4           426           B5
 
--- Worst Fit ---
Process No.  Process Size  Block No.
P1           212           B5
P2           417           B2
P3           112           B5
P4           426           Not Allocated
```

### Viva-Voce Questions

1. What is internal and external fragmentation?
2. Compare the time complexity of First Fit, Best Fit and Worst Fit.
3. What is compaction and how does it solve external fragmentation?
4. Why is Best Fit not always the best in practice?
5. How does paging avoid external fragmentation?
6. What is a hole (free block) in memory management?

## Program 9

**Page Replacement Algorithms — FIFO, LRU and Optimal**

| Aim | To implement and compare the FIFO, Least Recently Used (LRU) and Optimal page replacement algorithms used in demand paging, and to count the number of page faults produced by each for a given reference string. |
|---|---|

### Theory

In demand paging, when a referenced page is not in memory (a page fault) and all frames are full, the OS must select a victim page to replace, based on a page-replacement algorithm.

FIFO replaces the page that has been in memory the longest, regardless of usage — simple but can suffer from Belady's Anomaly (more frames causing more faults).

LRU replaces the page that has not been used for the longest period of time — approximates optimal behaviour based on the principle of locality of reference.

The Optimal (MIN) algorithm replaces the page that will not be used for the longest time in the future — it gives the theoretical minimum number of page faults but requires future knowledge and is used only as a benchmark.

### Program (Python)

```python
def is_present(frames, nf, page):
    for i in range(nf):
        if frames[i] == page:
            return True
    return False


def fifo(ref, nf):
    frames = [-1] * nf
    front, faults = 0, 0

    for page in ref:
        if not is_present(frames, nf, page):
            frames[front] = page
            front = (front + 1) % nf
            faults += 1
    print(f"FIFO Page Faults  = {faults}")


def lru(ref, nf):
    frames = [-1] * nf
    last_used = [0] * nf
    filled, faults = 0, 0

    for i, page in enumerate(ref):
        pos = -1
        for j in range(nf):
            if frames[j] == page:
                pos = j
                break

        if pos == -1:
            faults += 1
            if filled < nf:
                frames[filled] = page
                last_used[filled] = i
                filled += 1
            else:
                # find least recently used frame
                lru_idx = 0
                for j in range(1, nf):
                    if last_used[j] < last_used[lru_idx]:
                        lru_idx = j
                frames[lru_idx] = page
                last_used[lru_idx] = i
        else:
            last_used[pos] = i
    print(f"LRU Page Faults   = {faults}")


def optimal(ref, nf):
    n = len(ref)
    frames = [-1] * nf
    filled, faults = 0, 0

    for i in range(n):
        if is_present(frames, filled, ref[i]):
            continue

        faults += 1
        if filled < nf:
            frames[filled] = ref[i]
            filled += 1
            continue

        # find the frame whose page is used farthest in future (or never)
        replace_idx, farthest = -1, -1
        for j in range(nf):
            k = i + 1
            while k < n:
                if frames[j] == ref[k]:
                    break
                k += 1
            if k == n:                 # never used again
                replace_idx = j
                break
            if k > farthest:
                farthest = k
                replace_idx = j
        frames[replace_idx] = ref[i]
    print(f"Optimal Page Faults = {faults}")


def main():
    int(input("Enter number of pages in reference string: "))
    ref = list(map(int, input("Enter the reference string: ").split()))

    nf = int(input("Enter number of frames: "))

    fifo(ref, nf)
    lru(ref, nf)
    optimal(ref, nf)


main()
```

### Execution

```bash
python3 page_replacement.py
```

### Sample Output

```text
Enter number of pages in reference string: 12
Enter the reference string: 7 0 1 2 0 3 0 4 2 3 0 3
Enter number of frames: 3
FIFO Page Faults  = 10
LRU Page Faults   = 9
Optimal Page Faults = 7
```

### Viva-Voce Questions

1. What is a page fault?
2. What is Belady's Anomaly? Which algorithm suffers from it?
3. Why is the Optimal algorithm not implementable in practice?
4. What is thrashing and how is it related to page replacement?
5. How does the Least Frequently Used (LFU) algorithm differ from LRU?
6. What is the working-set model?

## Program 10

**Disk Scheduling Algorithms — FCFS, SSTF, SCAN and C-SCAN**

| Aim | To implement FCFS, SSTF, SCAN and C-SCAN disk scheduling algorithms and compute the total head movement for a given set of disk track requests. |
|---|---|

### Theory

Disk scheduling determines the order in which pending I/O requests (cylinder/track numbers) are serviced by the disk arm, to minimize total seek time (head movement).

FCFS services requests strictly in the order they arrive — fair but can result in a large total head movement.

SSTF (Shortest Seek Time First) always services the request closest to the current head position — reduces seek time but can cause starvation of far-away requests.

SCAN (elevator algorithm) moves the disk arm in one direction, servicing all requests along the way, until it reaches the end, then reverses direction.

C-SCAN (Circular SCAN) moves the arm in one direction servicing requests, then jumps back to the beginning without servicing on the return trip, giving more uniform wait times.

### Program (Python)

```python
def abs_diff(a, b):
    return a - b if a > b else b - a


def fcfs(req, head):
    total, cur = 0, head
    for r in req:
        total += abs_diff(cur, r)
        cur = r
    print(f"FCFS   total head movement = {total}")


def sstf(req, head):
    n = len(req)
    visited = [False] * n
    total, cur = 0, head
    for _ in range(n):
        idx, best = -1, 1 << 30
        for i in range(n):
            if not visited[i] and abs_diff(cur, req[i]) < best:
                best = abs_diff(cur, req[i])
                idx = i
        visited[idx] = True
        total += best
        cur = req[idx]
    print(f"SSTF   total head movement = {total}")


def scan(req, head, disk_size):
    n = len(req)
    arr = sorted(req + [head])
    idx = arr.index(head)

    total, cur = 0, head
    # go towards the higher end first
    for i in range(idx + 1, n + 1):
        total += abs_diff(cur, arr[i])
        cur = arr[i]
    total += abs_diff(cur, disk_size - 1)
    cur = disk_size - 1
    for i in range(idx - 1, -1, -1):
        total += abs_diff(cur, arr[i])
        cur = arr[i]

    print(f"SCAN   total head movement = {total}")


def cscan(req, head, disk_size):
    n = len(req)
    arr = sorted(req + [head])
    idx = arr.index(head)

    total, cur = 0, head
    for i in range(idx + 1, n + 1):
        total += abs_diff(cur, arr[i])
        cur = arr[i]
    total += abs_diff(cur, disk_size - 1)   # go to the end
    total += disk_size - 1                  # jump to 0 (cylinder 0)
    cur = 0
    for i in range(idx):
        total += abs_diff(cur, arr[i])
        cur = arr[i]

    print(f"C-SCAN total head movement = {total}")


def main():
    int(input("Enter number of requests: "))
    req = list(map(int, input("Enter the requests: ").split()))
    head = int(input("Enter initial head position: "))
    disk_size = int(input("Enter disk size (max cylinder + 1): "))

    fcfs(req, head)
    sstf(req, head)
    scan(req, head, disk_size)
    cscan(req, head, disk_size)


main()
```

### Execution

```bash
python3 disk_scheduling.py
```

### Sample Output

```text
Enter number of requests: 8
Enter the requests: 98 183 37 122 14 124 65 67
Enter initial head position: 53
Enter disk size (max cylinder + 1): 200
FCFS   total head movement = 640
SSTF   total head movement = 236
SCAN   total head movement = 331
C-SCAN total head movement = 382
```

### Viva-Voce Questions

1. What is seek time, and why do we try to minimize it?
2. Why can SSTF cause starvation?
3. What is the difference between SCAN and C-SCAN?
4. What is LOOK and C-LOOK, and how do they differ from SCAN/C-SCAN?
5. Why does C-SCAN give more uniform response time than SCAN?
6. What other factors besides seek time affect total disk access time?

## Program 11

**File Allocation Methods — Contiguous, Linked and Indexed Allocation**

| Aim | To simulate Contiguous, Linked and Indexed file allocation methods used by the operating system to allocate disk blocks to files, and to display the block allocation table for each. |
|---|---|

### Theory

Contiguous allocation stores each file as a set of contiguous blocks on the disk. It gives excellent sequential and direct access performance but suffers from external fragmentation and requires knowing the file size in advance.

Linked allocation stores each file as a linked list of disk blocks scattered anywhere on disk; each block contains a pointer to the next block. It eliminates external fragmentation but only supports efficient sequential access, and pointers consume space and are vulnerable to corruption.

Indexed allocation brings all block pointers of a file together into one index block. This supports efficient direct access and avoids external fragmentation, at the cost of extra space for the index block.

### Program (Python)

```python
MAXBLOCKS = 30

disk = [0] * MAXBLOCKS   # 0 = free, 1 = allocated


def reset_disk():
    for i in range(MAXBLOCKS):
        disk[i] = 0


def contiguous_allocation():
    reset_disk()
    print("\n--- Contiguous Allocation ---")
    nf = int(input("Enter number of files: "))

    for f in range(nf):
        start, length = map(int, input(
            f"File {f + 1} - starting block, length: ").split())

        ok = True
        for i in range(start, start + length):
            if i >= MAXBLOCKS or disk[i] == 1:
                ok = False
                break

        if not ok:
            print("Allocation failed: blocks not free/out of range.")
            continue
        for i in range(start, start + length):
            disk[i] = 1
        print(f"File {f + 1} allocated blocks {start} to {start + length - 1}")


def linked_allocation():
    reset_disk()
    print("\n--- Linked Allocation ---")
    nf = int(input("Enter number of files: "))

    for f in range(nf):
        length = int(input(f"File {f + 1} - number of blocks: "))

        print(f"File {f + 1} allocated blocks: ", end="")
        prev, count = -1, 0
        for i in range(MAXBLOCKS):
            if count >= length:
                break
            if disk[i] == 0:
                disk[i] = 1
                print(f"{i} ", end="")
                if prev != -1:
                    print("-> ", end="")
                prev = i
                count += 1
        print("(NULL)")
        if count < length:
            print("Warning: disk full, could not allocate all blocks.")


def indexed_allocation():
    reset_disk()
    print("\n--- Indexed Allocation ---")
    nf = int(input("Enter number of files: "))

    for f in range(nf):
        length = int(input(f"File {f + 1} - number of data blocks needed: "))

        index_block = -1
        for i in range(MAXBLOCKS):
            if disk[i] == 0:
                index_block = i
                disk[i] = 1
                break

        print(f"File {f + 1} - Index block: {index_block}, Data blocks: ", end="")
        count = 0
        for i in range(MAXBLOCKS):
            if count >= length:
                break
            if disk[i] == 0:
                disk[i] = 1
                print(f"{i} ", end="")
                count += 1
        print()


def main():
    print("Menu:\n1. Contiguous Allocation\n2. Linked Allocation")
    print("3. Indexed Allocation")
    choice = int(input("Enter choice: "))

    if choice == 1:
        contiguous_allocation()
    elif choice == 2:
        linked_allocation()
    elif choice == 3:
        indexed_allocation()
    else:
        print("Invalid choice")


main()
```

### Execution

```bash
python3 file_allocation.py
```

### Sample Output

```text
Menu:
1. Contiguous Allocation
2. Linked Allocation
3. Indexed Allocation
Enter choice: 3
 
--- Indexed Allocation ---
Enter number of files: 2
File 1 - number of data blocks needed: 4
File 1 - Index block: 0, Data blocks: 1 2 3 4 
File 2 - number of data blocks needed: 3
File 2 - Index block: 5, Data blocks: 6 7 8
```

### Viva-Voce Questions

1. Compare contiguous, linked and indexed allocation on the basis of direct access support.
2. What is external fragmentation, and which allocation method(s) suffer from it?
3. What is a File Allocation Table (FAT), and which allocation scheme does it relate to?
4. How does indexed allocation support random access better than linked allocation?
5. What is the problem when an index block itself becomes too large for one disk block (multilevel/linked index)?
6. What are the logical vs. physical views of a file?