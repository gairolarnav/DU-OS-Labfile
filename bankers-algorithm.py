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
