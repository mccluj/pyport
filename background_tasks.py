import multiprocessing
import psutil
import time

def target_function():
    # Your function logic here
    print(f"Working in process {multiprocessing.current_process().name}")
    time.sleep(5)  # Simulate long-running task

def set_process_priority(low=True):
    p = psutil.Process()  # Current process
    if low:
        p.nice(psutil.IDLE_PRIORITY_CLASS)
    else:
        p.nice(psutil.NORMAL_PRIORITY_CLASS)

def run_function_with_priority(func, priority='low'):
    process = multiprocessing.Process(target=func)
    process.start()
    
    # Wait a bit for the process to start
    time.sleep(0.1)
    
    # Set the process priority
    if priority == 'low':
        set_process_priority(low=True)
    else:
        set_process_priority(low=False)
    
    return process

if __name__ == "__main__":
    processes = []
    for _ in range(5):  # Example: Launch 5 processes
        p = run_function_with_priority(target_function, priority='low')
        processes.append(p)
    
    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All processes completed.")
