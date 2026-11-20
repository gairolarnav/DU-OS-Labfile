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
