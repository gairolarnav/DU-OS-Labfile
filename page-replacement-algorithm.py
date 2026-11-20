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
