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
