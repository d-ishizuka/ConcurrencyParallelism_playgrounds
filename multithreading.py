import os
import time
import threading
from threading import Thread

def cpu_waster(i: int) -> None:
    name = threading.current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)

def display_threads() -> None:
    print("-" * 10)
    print(f"Current process PID: {os.getpid()}")
    print(f"Thread Count: {threading.active_count()}")
    print("Active threads:")
    for thread in threading.enumerate():
        print(thread)

def main(num_threads: int) -> None:
    start_time = time.time()  # 開始時刻を記録
    
    display_threads()
    
    print(f"Starting {num_threads} CPU wasters...")
    threads = []  # スレッドを格納するリスト
    
    for i in range(num_threads):
        thread = Thread(target=cpu_waster, args=(i,))
        threads.append(thread)  # スレッドをリストに追加
        thread.start()
    
    display_threads()
    
    # すべてのスレッドの終了を待機
    for thread in threads:
        thread.join()
    
    end_time = time.time()  # 終了時刻を記録
    print(f"\n実行時間: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
    num_threads = 5
    main(num_threads)