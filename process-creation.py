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
