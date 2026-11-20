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
