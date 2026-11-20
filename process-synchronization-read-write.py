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
