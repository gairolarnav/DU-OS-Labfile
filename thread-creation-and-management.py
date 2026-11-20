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
