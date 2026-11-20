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
