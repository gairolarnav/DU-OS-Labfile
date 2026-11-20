# Operating Systems Lab (CEC301/CSC301)

Practical file for Operating Systems, B.Tech / B.Sc. (CSE), Third Year. All programs are written in Python 3.

**Submitted by:** Arnav Gairola | **Roll No.:** 2472020

The full lab file (aim, theory, code, sample output and viva questions) is in [Lab-File.md](Lab-File.md).

## Programs

| # | Program | File |
|---|---------|------|
| 1 | Linux system calls: process creation using `fork()`, `exec()` and `wait()` | `fork_exec.py` |
| 2 | Thread creation and management | `thread_sum.py` |
| 3 | CPU scheduling: FCFS, SJF, Priority and Round Robin | `scheduling.py` |
| 4 | Producer-Consumer problem using semaphores | `producer_consumer.py` |
| 5 | Readers-Writers problem using semaphores | `readers_writers.py` |
| 6 | Dining Philosophers problem using semaphores | `dining_philosophers.py` |
| 7 | Deadlock avoidance using Banker's Algorithm | `bankers.py` |
| 8 | Contiguous memory allocation: First Fit, Best Fit, Worst Fit | `memory_allocation.py` |
| 9 | Page replacement: FIFO, LRU and Optimal | `page_replacement.py` |
| 10 | Disk scheduling: FCFS, SSTF, SCAN and C-SCAN | `disk_scheduling.py` |
| 11 | File allocation: Contiguous, Linked and Indexed | `file_allocation.py` |

## Requirements

- Python 3 (tested with 3.12)
- Program 1 uses `os.fork()`, so it runs on Linux, macOS or WSL, not on native Windows.

## How to run

```bash
python3 <file-name>.py
```

For example:

```bash
python3 scheduling.py
```

Programs 3 and 7 to 11 ask for input at runtime. Sample inputs and outputs are in [OS-Lab-File.md](OS-Lab-File.md).

## Notes

- Programs 2, 4, 5 and 6 use multiple threads, so the order of output lines can change between runs.